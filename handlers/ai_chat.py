import os
import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import main_menu

router = Router()

class SearchState(StatesGroup):
    waiting = State()

BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")
_cache = None

def load_texts() -> dict:
    global _cache
    if _cache is not None:
        return _cache
    result = {}
    if not os.path.exists(BOOKS_DIR):
        _cache = {}
        return {}
    for filename in sorted(os.listdir(BOOKS_DIR)):
        if not filename.lower().endswith(".txt"):
            continue
        filepath = os.path.join(BOOKS_DIR, filename)
        content = None
        for enc in ["utf-8", "utf-8-sig", "cp1251", "cp1252", "latin-1"]:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    content = f.read().strip()
                if content:
                    break
            except Exception:
                continue
        if content:
            title = filename.replace(".txt", "").replace("_", " ").replace("-", " ").title()
            result[title] = content
    _cache = result
    return result

def search_texts(query: str, max_results: int = 3) -> list:
    texts = load_texts()
    if not texts:
        return []
    
    # Savol belgisini olib tashlash
    query = query.strip().rstrip("?").rstrip("؟")
    words = [w for w in re.findall(r'\w+', query.lower()) if len(w) > 2]
    if not words:
        return []
    
    results = []
    for title, content in texts.items():
        paragraphs = [p.strip() for p in content.split('\n') if len(p.strip()) > 40]
        for para in paragraphs:
            para_lower = para.lower()
            # Har bir so'z nechta marta uchraydi — og'irlik berish
            score = 0
            for w in words:
                count = para_lower.count(w)
                score += count * (2 if len(w) > 4 else 1)  # Uzun so'zlar muhimroq
            
            # Faqat aniq mos kelganlarni olish
            if score >= len(words):  # Barcha so'zlar bo'lishi kerak
                results.append((score, title, para))
    
    # Agar hamma so'z bo'lmasa, kamida bitta uzun so'z bo'lsa
    if not results:
        long_words = [w for w in words if len(w) > 3]
        for title, content in texts.items():
            paragraphs = [p.strip() for p in content.split('\n') if len(p.strip()) > 40]
            for para in paragraphs:
                para_lower = para.lower()
                score = sum(para_lower.count(w) * 2 for w in long_words)
                if score > 0:
                    results.append((score, title, para))
    
    results.sort(key=lambda x: x[0], reverse=True)
    # Takroriy paragraflarni olib tashlash
    seen = set()
    unique = []
    for score, title, para in results:
        key = para[:50]
        if key not in seen:
            seen.add(key)
            unique.append((score, title, para))
    
    return unique[:max_results]

def format_answer(query: str, results: list) -> str:
    """Natijalarni aniq va chiroyli formatlash"""
    if not results:
        return (
            f"❌ *'{query}'* haqida ma'lumot topilmadi.\n\n"
            "💡 Boshqa so'z bilan sinab ko'ring:\n"
            "• `tug'ilgan yili`\n"
            "• `she'rlari`\n"
            "• `Shum bola`"
        )
    
    # Bitta natija bo'lsa — to'liq javob
    if len(results) == 1:
        _, title, para = results[0]
        return f"📖 *{title}*\n\n{para}\n\n_Manba: {title}_"
    
    # Ko'p natija — ro'yxat
    response = f"📚 *'{query}'* haqida:\n\n"
    for i, (_, title, para) in enumerate(results, 1):
        short = para[:300] + "..." if len(para) > 300 else para
        response += f"*{i}.* {short}\n\n{'─'*15}\n\n"
    return response

@router.message(F.text == "🔍 Qidirish")
async def start_search(message: Message, state: FSMContext):
    global _cache
    _cache = None
    texts = load_texts()
    count = len(texts)
    total_chars = sum(len(v) for v in texts.values())

    await state.set_state(SearchState.waiting)
    await message.answer(
        "🔍 *Qidirish*\n\n"
        f"📚 Yuklangan fayllar: *{count} ta*\n"
        f"📝 Jami matn: *{total_chars:,} belgi*\n\n"
        "Qidirmoqchi bo'lgan so'zni yozing:\n\n"
        "💡 *Misol:*\n"
        "• `shum bola`\n"
        "• `she'r`\n"
        "• `1903`\n"
        "• `Toshkent`\n\n"
        "❌ Bekor qilish: /stop",
        parse_mode="Markdown"
    )

@router.message(F.text == "/stop")
async def stop_search(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Qidirish tugatildi.", reply_markup=main_menu())

@router.message(SearchState.waiting)
async def do_search(message: Message):
    query = message.text.strip()
    if not query:
        return

    searching_msg = await message.answer("🔍 Qidiryapman...")
    results = search_texts(query, max_results=3)
    await searching_msg.delete()

    response = format_answer(query, results)

    if len(response) > 4096:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await message.answer(chunk, parse_mode="Markdown")
    else:
        await message.answer(
            response + "\n\n💬 _Yangi so'z yozing yoki /stop bosing_",
            parse_mode="Markdown"
        )
