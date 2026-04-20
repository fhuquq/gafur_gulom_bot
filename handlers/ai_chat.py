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

# ═══════════════════════════════════════
# FAYLLARNI O'QISH
# ═══════════════════════════════════════

def load_texts() -> dict:
    """Barcha TXT fayllarni o'qib qaytarish {fayl_nomi: matn}"""
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

# ═══════════════════════════════════════
# QIDIRUV TIZIMI
# ═══════════════════════════════════════

def get_snippet(content: str, pos: int, radius: int = 500) -> str:
    """Topilgan pozitsiyadan radius belgi oldin va keyin matn olish"""
    start = max(0, pos - radius)
    end = min(len(content), pos + radius)

    # Qatorning boshidan boshlash
    if start > 0:
        nl = content.rfind('\n', 0, start)
        if nl != -1:
            start = nl + 1

    # Qatorning oxirida tugatish
    if end < len(content):
        nl = content.find('\n', end)
        if nl != -1:
            end = nl

    snippet = content[start:end].strip()
    prefix = "...\n" if start > 0 else ""
    suffix = "\n..." if end < len(content) else ""
    return prefix + snippet + suffix

def search_texts(query: str) -> list:
    """
    Aqlli qidiruv:
    1. Avval to'liq ibora sifatida qidiradi
    2. Topilmasa, har bir so'zni alohida qidiradi
    """
    texts = load_texts()
    if not texts:
        return []

    query_clean = query.strip().rstrip("?؟").strip()
    query_lower = query_clean.lower()

    results = []

    # === 1-usul: TO'LIQ IBORA QIDIRISH ===
    for title, content in texts.items():
        content_lower = content.lower()
        pos = content_lower.find(query_lower)
        if pos != -1:
            # Necha marta uchraydi
            count = content_lower.count(query_lower)
            snippet = get_snippet(content, pos, radius=600)
            results.append((count * 10, title, snippet))  # Ko'p uchraydi = yuqori ball

    # === 2-usul: SO'ZLARNI ALOHIDA QIDIRISH (1-usul topilmasa) ===
    if not results:
        words = [w for w in re.findall(r'\w+', query_lower) if len(w) > 2]
        if not words:
            return []

        for title, content in texts.items():
            content_lower = content.lower()

            # Eng uzun so'zni topish (muhimroq)
            best_word = max(words, key=lambda w: len(w))
            best_pos = content_lower.find(best_word)

            if best_pos == -1:
                continue

            # Hammasi bormi tekshirish
            score = sum(content_lower.count(w) for w in words if w in content_lower)
            snippet = get_snippet(content, best_pos, radius=600)
            results.append((score, title, snippet))

    # Ballga ko'ra saralash, takrorlarni olib tashlash
    results.sort(key=lambda x: x[0], reverse=True)
    seen = set()
    unique = []
    for score, title, snippet in results:
        key = snippet[:80].strip()
        if key not in seen:
            seen.add(key)
            unique.append((score, title, snippet))

    return unique[:3]

# ═══════════════════════════════════════
# FORMATLASH
# ═══════════════════════════════════════

def format_answer(query: str, results: list) -> str:
    if not results:
        return (
            f"❌ *'{query}'* haqida hech narsa topilmadi.\n\n"
            "💡 Boshqa so'z bilan sinab ko'ring:\n"
            "• Isim: `Toshbibi`, `G'afur G'ulom`\n"
            "• Asar: `Shum bola`, `Navoiy`\n"
            "• Mavzu: `she'r`, `urush`, `1903`"
        )

    if len(results) == 1:
        _, title, snippet = results[0]
        return f"📖 *{title}*\n\n{snippet}"

    response = f"📚 *'{query}'* bo'yicha *{len(results)} ta* natija:\n\n"
    for i, (_, title, snippet) in enumerate(results, 1):
        short = snippet[:800] + "\n..." if len(snippet) > 800 else snippet
        response += f"*{i}. {title}*\n{short}\n\n{'─' * 20}\n\n"
    return response

# ═══════════════════════════════════════
# HANDLERS
# ═══════════════════════════════════════

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
        f"📝 Jami matn hajmi: *{total:,} belgi*\n\n"
        "So'z yoki ibora yozing:\n\n"
        "💡 *Misol:*\n"
        "• `Toshbibi` — shaxs ismi\n"
        "• `Sen yetim emassan` — asar nomi\n"
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

    wait_msg = await message.answer("🔍 Qidiryapman...")
    results = search_texts(query)
    await wait_msg.delete()

    response = format_answer(query, results)
    response += "\n\n💬 _Yangi so'z yozing yoki /stop bosing_"

    if len(response) > 4096:
        for chunk in [response[i:i+4000] for i in range(0, len(response), 4000)]:
            await message.answer(chunk, parse_mode="Markdown")
    else:
        await message.answer(response, parse_mode="Markdown")
