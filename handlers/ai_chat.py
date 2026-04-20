import os
import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import main_menu

router = Router()

class SearchState(StatesGroup):
    waiting = State()

BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")
_cache = None

def load_texts() -> dict:
    """Barcha TXT fayllarni o'qib, lug'at shaklida qaytarish {title: content}"""
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

def search_in_texts(query: str, max_results: int = 5) -> list:
    """Kalit so'z bo'yicha qidirish — mos paragraflarni qaytarish"""
    texts = load_texts()
    if not texts:
        return []

    query_lower = query.lower()
    words = [w for w in re.findall(r'\w+', query_lower) if len(w) > 2]
    if not words:
        return []

    results = []
    for title, content in texts.items():
        paragraphs = [p.strip() for p in content.split('\n') if len(p.strip()) > 30]
        for para in paragraphs:
            para_lower = para.lower()
            score = sum(1 for w in words if w in para_lower)
            if score > 0:
                results.append((score, title, para))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:max_results]

def get_section(keyword: str, max_chars: int = 2000) -> str:
    """Muayyan mavzu bo'yicha matn qismi olish"""
    texts = load_texts()
    if not texts:
        return ""

    keyword_lower = keyword.lower()
    found_parts = []

    for title, content in texts.items():
        paragraphs = [p.strip() for p in content.split('\n') if len(p.strip()) > 20]
        for para in paragraphs:
            if keyword_lower in para.lower():
                found_parts.append(para)
            if sum(len(p) for p in found_parts) > max_chars:
                break

    return "\n\n".join(found_parts[:8])

# ═══════════════════════════════════
# HANDLERS
# ═══════════════════════════════════

@router.message(F.text == "🔍 Qidirish")
async def start_search(message: Message, state: FSMContext):
    global _cache
    _cache = None
    texts = load_texts()
    count = len(texts)

    await state.set_state(SearchState.waiting)
    await message.answer(
        "🔍 *Qidirish rejimi*\n\n"
        f"📚 Yuklangan manbalar: *{count} ta fayl*\n\n"
        "Qidirmoqchi bo'lgan so'zni yozing:\n\n"
        "💡 *Misol:*\n"
        "• `shum bola`\n"
        "• `she'r`\n"
        "• `Toshkent`\n"
        "• `1903`\n\n"
        "❌ Bekor qilish: /stop",
        parse_mode="Markdown"
    )

@router.message(F.text == "/stop")
async def stop_search(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Tugadi.", reply_markup=main_menu())

@router.message(SearchState.waiting)
async def do_search(message: Message, state: FSMContext):
    query = message.text.strip()
    if not query:
        return

    searching_msg = await message.answer("🔍 Qidiryapman...")
    results = search_in_texts(query, max_results=5)
    await searching_msg.delete()

    if not results:
        await message.answer(
            f"❌ *'{query}'* bo'yicha hech narsa topilmadi.\n\n"
            "Boshqa so'z bilan sinab ko'ring yoki /stop bosing.",
            parse_mode="Markdown"
        )
        return

    response = f"🔍 *'{query}'* bo'yicha natijalar:\n\n"
    for i, (score, title, para) in enumerate(results, 1):
        # Paragrafni 300 belgida kesish
        short = para[:300] + "..." if len(para) > 300 else para
        response += f"*{i}. [{title}]*\n{short}\n\n"
        response += "─" * 20 + "\n\n"

    response += "💬 _Yangi so'z yozing yoki /stop bosing_"

    if len(response) > 4096:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await message.answer(chunk, parse_mode="Markdown")
    else:
        await message.answer(response, parse_mode="Markdown")

# Bo'limlar bo'yicha ma'lumot
@router.callback_query(F.data == "section_bio")
async def section_bio(callback: CallbackQuery):
    text = get_section("tug'ilgan") or get_section("hayot") or get_section("1903")
    if text:
        await callback.message.answer(
            f"📜 *Biografiyadan:*\n\n{text[:3000]}",
            parse_mode="Markdown"
        )
    else:
        await callback.message.answer("⚠️ Biografiya matni topilmadi. TXT fayl qo'shing.")
    await callback.answer()

@router.callback_query(F.data == "section_poems")
async def section_poems(callback: CallbackQuery):
    text = get_section("she'r") or get_section("shеr") or get_section("lirik")
    if text:
        await callback.message.answer(
            f"🎭 *She'rlardan:*\n\n{text[:3000]}",
            parse_mode="Markdown"
        )
    else:
        await callback.message.answer("⚠️ She'rlar matni topilmadi. TXT fayl qo'shing.")
    await callback.answer()

@router.callback_query(F.data == "section_works")
async def section_works(callback: CallbackQuery):
    text = get_section("asar") or get_section("roman") or get_section("qissa")
    if text:
        await callback.message.answer(
            f"📚 *Asarlardan:*\n\n{text[:3000]}",
            parse_mode="Markdown"
        )
    else:
        await callback.message.answer("⚠️ Asarlar matni topilmadi. TXT fayl qo'shing.")
    await callback.answer()

@router.callback_query(F.data == "section_stories")
async def section_stories(callback: CallbackQuery):
    text = get_section("hikoy") or get_section("voqea")
    if text:
        await callback.message.answer(
            f"📝 *Hikoyalardan:*\n\n{text[:3000]}",
            parse_mode="Markdown"
        )
    else:
        await callback.message.answer("⚠️ Hikoyalar matni topilmadi. TXT fayl qo'shing.")
    await callback.answer()

# Umumiy matn — qidiruvga yo'naltirish
@router.message(F.text & ~F.text.startswith("/"))
async def handle_general(message: Message, state: FSMContext):
    skip = [
        "📚 Kitoblar", "🎧 Audio hikoyalar", "📖 Asarlari haqida",
        "ℹ️ Tarjimayi hol", "🎭 She'rlar", "❓ Yordam", "🔍 Qidirish"
    ]
    if message.text in skip:
        return

    # Avtomatik qidirish
    results = search_in_texts(message.text, max_results=3)
    if results:
        response = f"🔍 *'{message.text}'* bo'yicha topildi:\n\n"
        for score, title, para in results:
            short = para[:400] + "..." if len(para) > 400 else para
            response += f"📌 *[{title}]*\n{short}\n\n"
        await message.answer(response, parse_mode="Markdown", reply_markup=main_menu())
    else:
        await message.answer(
            "❓ Bu haqda ma'lumot topilmadi.\n\n"
            "🔍 *Qidirish* tugmasini bosib, boshqa so'z bilan sinab ko'ring.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
