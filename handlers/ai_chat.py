import os
import re
from aiogram import Router, F
from aiogram.types import Message
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

def extract_snippet(content: str, word: str, radius: int = 600) -> str:
    """So'z topilgan joydan radius belgi oldin va keyin matn olish"""
    idx = content.lower().find(word.lower())
    if idx == -1:
        return ""
    
    start = max(0, idx - radius)
    end = min(len(content), idx + len(word) + radius)

    # Eng yaqin yangi qatordan boshlansin
    if start > 0:
        border = content.rfind('\n', 0, start)
        if border > 0:
            start = border + 1

    # Eng yaqin yangi qatorda tugasin
    if end < len(content):
        border = content.find('\n', end)
        if border > 0:
            end = border

    snippet = content[start:end].strip()
    prefix = "...\n" if start > 0 else ""
    suffix = "\n..." if end < len(content) else ""
    return prefix + snippet + suffix

def search_texts(query: str, max_results: int = 3) -> list:
    texts = load_texts()
    if not texts:
        return []

    query = query.strip().rstrip("?").rstrip("؟")
    words = [w for w in re.findall(r'\w+', query.lower()) if len(w) > 2]
    if not words:
        return []

    results = []
    for title, content in texts.items():
        content_lower = content.lower()

        score = 0
        found_words = []
        for w in words:
            if w in content_lower:
                cnt = content_lower.count(w)
                score += cnt * (2 if len(w) > 4 else 1)
                found_words.append(w)

        if not found_words:
            continue

        # Eng uzun (muhim) so'z atrofidan snippet olish
        best_word = max(found_words, key=lambda w: len(w))
        snippet = extract_snippet(content, best_word, radius=600)

        if snippet:
            results.append((score, title, snippet))

    results.sort(key=lambda x: x[0], reverse=True)

    seen = set()
    unique = []
    for score, title, snippet in results:
        key = snippet[3:63]  # prefix "..." ni o'tkazib yuborish
        if key not in seen:
            seen.add(key)
            unique.append((score, title, snippet))

    return unique[:max_results]

def format_answer(query: str, results: list) -> str:
    if not results:
        return (
            f"❌ *'{query}'* haqida ma'lumot topilmadi.\n\n"
            "💡 Boshqa so'z bilan sinab ko'ring:\n"
            "• `tug'ilgan yili`\n"
            "• `she'rlari`\n"
            "• `Shum bola`"
        )

    if len(results) == 1:
        _, title, snippet = results[0]
        return f"📖 *{title}*\n\n{snippet}"

    response = f"📚 *'{query}'* bo'yicha natijalar:\n\n"
    for i, (_, title, snippet) in enumerate(results, 1):
        short = snippet[:700] + "\n..." if len(snippet) > 700 else snippet
        response += f"*{i}. {title}*\n{short}\n\n{'─'*15}\n\n"
    return response

@router.message(F.text == "🔍 Qidirish")
async def start_search(message: Message, state: FSMContext):
    global _cache
    _cache = None
    texts = load_texts()
    count = len(texts)
    total = sum(len(v) for v in texts.values())

    await state.set_state(SearchState.waiting)
    await message.answer(
        "🔍 *Qidirish*\n\n"
        f"📚 Yuklangan fayllar: *{count} ta*\n"
        f"📝 Jami matn: *{total:,} belgi*\n\n"
        "Qidirmoqchi bo'lgan so'z yoki ismni yozing:\n\n"
        "💡 *Misol:*\n"
        "• `Toshbibi` — shaxs ismi\n"
        "• `Turksib` — mavzu\n"
        "• `1918` — sana\n"
        "• `Shum bola` — asar nomi\n\n"
        "❌ Tugatish: /stop",
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
    results = search_texts(query)
    await searching_msg.delete()

    response = format_answer(query, results)
    response += "\n\n💬 _Yangi so'z yozing yoki /stop bosing_"

    if len(response) > 4096:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await message.answer(chunk, parse_mode="Markdown")
    else:
        await message.answer(response, parse_mode="Markdown")
