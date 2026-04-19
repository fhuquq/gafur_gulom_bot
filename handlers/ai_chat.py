import os
import re
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import main_menu, cancel_button
from data.gafur_data import SYSTEM_PROMPT

router = Router()

class ChatStates(StatesGroup):
    in_conversation = State()

conversation_histories = {}

# ═══════════════════════════════════════
# RAG — KITOBLARDAN MA'LUMOT O'QISH
# ═══════════════════════════════════════

BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")
_knowledge_cache = None

def load_all_texts() -> str:
    global _knowledge_cache
    if _knowledge_cache is not None:
        return _knowledge_cache

    texts = []
    if not os.path.exists(BOOKS_DIR):
        _knowledge_cache = ""
        return ""

    for filename in sorted(os.listdir(BOOKS_DIR)):
        filepath = os.path.join(BOOKS_DIR, filename)
        if filename.lower().endswith(".txt"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content:
                    title = filename.replace(".txt", "").replace("_", " ").title()
                    texts.append(f"\n\n{'='*50}\nASAR: {title}\n{'='*50}\n{content}")
            except Exception:
                pass

    _knowledge_cache = "\n".join(texts)
    return _knowledge_cache

def search_relevant_chunks(query: str, max_chars: int = 3000) -> str:
    all_text = load_all_texts()
    if not all_text:
        return ""

    query_lower = query.lower()
    words = [w for w in re.findall(r'\w+', query_lower) if len(w) > 2]

    if not words:
        return all_text[:max_chars]

    paragraphs = [p.strip() for p in all_text.split('\n') if p.strip()]

    scored = []
    for para in paragraphs:
        para_lower = para.lower()
        score = sum(1 for w in words if w in para_lower)
        if score > 0:
            scored.append((score, para))

    scored.sort(key=lambda x: x[0], reverse=True)
    result_parts = []
    total_chars = 0

    for score, para in scored:
        if total_chars + len(para) > max_chars:
            break
        result_parts.append(para)
        total_chars += len(para)

    return "\n\n".join(result_parts) if result_parts else all_text[:max_chars]

def build_system_prompt_with_context(user_question: str) -> str:
    context = search_relevant_chunks(user_question)

    if context:
        return f"""{SYSTEM_PROMPT}

{'='*60}
MUHIM QOIDA: Quyidagi haqiqiy asar matnlaridan foydalaning!
Faqat shu ma'lumotlarga asoslanib javob bering.
Agar savol bu ma'lumotlarda bo'lmasa — "Bu haqda aniq ma'lumot topilmadi" deng.
HECH QACHON o'zingizdan to'qib chiqarmang!

MANBA MATNLAR:
{context}
{'='*60}"""
    else:
        return f"""{SYSTEM_PROMPT}

ESLATMA: Kitob matnlari hali yuklanmagan.
Faqat o'zingizda bor ishonchli ma'lumotlarni ayting.
Bilmasangiz — "Aniq ma'lumot yo'q" deng. Hech narsa to'qib chiqarmang!"""

# ═══════════════════════════════════════
# GROQ API
# ═══════════════════════════════════════

async def ask_ai(user_id: int, user_message: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY topilmadi!")

    if user_id not in conversation_histories:
        conversation_histories[user_id] = []

    history = conversation_histories[user_id]
    system_with_context = build_system_prompt_with_context(user_message)
    history.append({"role": "user", "content": user_message})

    if len(history) > 16:
        history = history[-16:]
        conversation_histories[user_id] = history

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_with_context},
            *history
        ],
        "max_tokens": 1024,
        "temperature": 0.3
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                raise Exception(f"Groq API xatosi ({resp.status}): {error_text}")
            data = await resp.json()
            ai_response = data["choices"][0]["message"]["content"]

    history.append({"role": "assistant", "content": ai_response})
    conversation_histories[user_id] = history
    return ai_response

# ═══════════════════════════════════════
# HANDLERS
# ═══════════════════════════════════════

@router.message(F.text == "🤖 AI bilan suhbat")
async def start_ai_chat(message: Message, state: FSMContext):
    global _knowledge_cache
    _knowledge_cache = None
    texts = load_all_texts()
    books_count = texts.count("ASAR:") if texts else 0

    user_id = message.from_user.id
    conversation_histories[user_id] = []

    await state.set_state(ChatStates.in_conversation)
    await message.answer(
        "🤖 *AI Suhbat rejimi*\n\n"
        f"📚 Yuklangan asarlar: *{books_count} ta*\n\n"
        "G'afur G'ulom haqida istalgan savolingizni bering.\n"
        "AI faqat haqiqiy ma'lumotlarga asoslanib javob beradi.\n\n"
        "💡 *Misol:*\n"
        "• Shum bola asarini tahlil qil\n"
        "• G'afur G'ulomning she'rlarini ayt\n"
        "• Navoiy romani haqida gapir\n\n"
        "❌ Tugatish: /stop",
        parse_mode="Markdown",
        reply_markup=cancel_button()
    )

@router.message(F.text == "/stop")
@router.callback_query(F.data == "cancel_chat")
async def cancel_chat(message_or_callback, state: FSMContext):
    await state.clear()
    if isinstance(message_or_callback, CallbackQuery):
        msg = message_or_callback.message
        await message_or_callback.answer()
    else:
        msg = message_or_callback
    await msg.answer("✅ Suhbat tugatildi.", reply_markup=main_menu())

@router.message(ChatStates.in_conversation)
async def handle_ai_message(message: Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("❗ Iltimos, savol yozing.")
        return

    thinking_msg = await message.answer("🔍 Qidiryapman va o'ylamoqda...")
    try:
        ai_response = await ask_ai(message.from_user.id, message.text.strip())
        await thinking_msg.delete()

        response_text = f"🤖 *AI Javobi:*\n\n{ai_response}\n\n─────────────\n💬 _Davom etish uchun savol bering_"

        if len(response_text) > 4096:
            chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
            for chunk in chunks:
                await message.answer(chunk, parse_mode="Markdown")
        else:
            await message.answer(response_text, parse_mode="Markdown")

    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"❌ Xato: {str(e)}\n\nQayta urinib ko'ring.")

@router.message(F.text.endswith("?"))
async def handle_question(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == ChatStates.in_conversation:
        return

    thinking_msg = await message.answer("🔍 Qidiryapman...")
    try:
        ai_response = await ask_ai(message.from_user.id, message.text)
        await thinking_msg.delete()
        await message.answer(
            f"🤖 *AI Javobi:*\n\n{ai_response}",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"❌ Xato: {str(e)}", reply_markup=main_menu())
