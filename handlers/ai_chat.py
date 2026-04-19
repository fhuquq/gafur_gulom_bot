import os
import aiohttp
import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import main_menu, cancel_button
from data.gafur_data import SYSTEM_PROMPT

router = Router()

class ChatStates(StatesGroup):
    waiting_for_question = State()
    in_conversation = State()

# Suhbat tarixini saqlash
conversation_histories = {}

async def ask_claude(user_id: int, user_message: str) -> str:
    """Google Gemini AI ga savol yuborish va javob olish (BEPUL)"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY topilmadi!")

    # Suhbat tarixini olish yoki yangi boshlash
    if user_id not in conversation_histories:
        conversation_histories[user_id] = []

    history = conversation_histories[user_id]

    # Gemini uchun tarix formati
    gemini_history = []
    for msg in history[-18:]:  # oxirgi 18 ta xabar
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    # Yangi xabarni qo'shish
    gemini_history.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    # Gemini API URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": gemini_history,
        "generationConfig": {
            "maxOutputTokens": 1024,
            "temperature": 0.7
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                raise Exception(f"Gemini API xatosi ({resp.status}): {error_text}")
            
            data = await resp.json()
            ai_response = data["candidates"][0]["content"]["parts"][0]["text"]

    # Tarixni yangilash
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": ai_response})

    # 20 xabardan oshmasin
    if len(history) > 20:
        conversation_histories[user_id] = history[-20:]
    else:
        conversation_histories[user_id] = history

    return ai_response

# AI suhbat tugmasi
@router.message(F.text == "🤖 AI bilan suhbat")
async def start_ai_chat(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Suhbat tarixini tozalash
    if user_id in conversation_histories:
        conversation_histories[user_id] = []
    
    await state.set_state(ChatStates.in_conversation)
    
    await message.answer(
        "🤖 *AI Suhbat rejimi faollashdi!*\n\n"
        "Endi G'afur G'ulom haqida istalgan savolingizni bering.\n"
        "Suhbat davom etadi va kontekst saqlanadi.\n\n"
        "💡 *Misol savollar:*\n"
        "• Shum bola asarining asosiy mavzusi nima?\n"
        "• G'afur G'ulom qachon vafot etgan?\n"
        "• Uning eng mashhur she'ri qaysi?\n\n"
        "❌ Suhbatni tugatish uchun /stop yozing",
        parse_mode="Markdown",
        reply_markup=cancel_button()
    )

# Suhbatni to'xtatish
@router.message(F.text == "/stop")
@router.callback_query(F.data == "cancel_chat")
async def cancel_chat(message_or_callback, state: FSMContext):
    await state.clear()
    
    if isinstance(message_or_callback, CallbackQuery):
        msg = message_or_callback.message
        await message_or_callback.answer()
    else:
        msg = message_or_callback
    
    await msg.answer(
        "✅ Suhbat tugatildi.\nAsosiy menyuga qaytdingiz.",
        reply_markup=main_menu()
    )

# AI suhbat davomida istalgan xabar
@router.message(ChatStates.in_conversation)
async def handle_ai_message(message: Message, state: FSMContext):
    user_text = message.text.strip()
    
    if not user_text:
        await message.answer("❗ Iltimos, savol yozing.")
        return
    
    # Yuklanmoqda...
    thinking_msg = await message.answer("🤔 O'ylamoqda...")
    
    try:
        # AI javobini olish
        ai_response = await ask_claude(message.from_user.id, user_text)
        
        # Yuklanmoqda xabarini o'chirish
        await thinking_msg.delete()
        
        # AI javobini yuborish
        response_text = f"🤖 *AI Javobi:*\n\n{ai_response}\n\n─────────────────\n💬 _Davom etish uchun savol bering_"
        
        # Xabar uzun bo'lsa, bo'laklarga bo'lish
        if len(response_text) > 4096:
            chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
            for chunk in chunks:
                await message.answer(chunk, parse_mode="Markdown")
        else:
            await message.answer(response_text, parse_mode="Markdown")
            
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"❌ Xato: {str(e)}\n\nQayta urinib ko'ring.")

# Oddiy savol (AI rejimida bo'lmasa ham)
@router.message(F.text.startswith("?") | F.text.endswith("?"))
async def handle_question(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    # Agar allaqachon AI rejimida bo'lsa, qayta ishlamaslik
    if current_state == ChatStates.in_conversation:
        return
    
    thinking_msg = await message.answer("🤔 O'ylamoqda...")
    
    try:
        ai_response = await ask_claude(message.from_user.id, message.text)
        await thinking_msg.delete()
        
        await message.answer(
            f"🤖 *AI Javobi:*\n\n{ai_response}",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    except Exception as e:
        await thinking_msg.delete()
        await message.answer(f"❌ Xato: {str(e)}")
