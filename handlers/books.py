import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import main_menu
from data.gafur_data import NOVELS_INFO

router = Router()

BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "audio")

BOOK_EMOJIS = ["📗", "📘", "📙", "📕", "📓", "📒", "📔", "📖"]

# PDF va EPUB — foydalanuvchiga ko'rsatiladi
BOOK_EXTENSIONS = [".pdf", ".epub", ".docx"]
# TXT — faqat AI uchun (ko'rsatilmaydi)
AI_EXTENSIONS = [".txt"]
# Audio
AUDIO_EXTENSIONS = [".mp3", ".ogg", ".m4a", ".wav"]

def get_files(directory: str, extensions: list) -> list:
    if not os.path.exists(directory):
        return []
    return sorted([f for f in os.listdir(directory)
                   if any(f.lower().endswith(ext) for ext in extensions)])

def filename_to_title(filename: str) -> str:
    name = os.path.splitext(filename)[0]
    return name.replace("_", " ").replace("-", " ").title()

def safe(filename: str) -> str:
    return filename.replace(".", "_dot_").replace(" ", "__")

def unsafe(safe_name: str) -> str:
    return safe_name.replace("_dot_", ".").replace("__", " ")

def find_file(safe_name: str, directory: str, extensions: list) -> str | None:
    original = unsafe(safe_name)
    for f in get_files(directory, extensions):
        if safe(f) == safe_name or f == original:
            return f
    return None

def books_keyboard() -> InlineKeyboardMarkup:
    files = get_files(BOOKS_DIR, BOOK_EXTENSIONS)
    buttons = []
    for i, f in enumerate(files):
        emoji = BOOK_EMOJIS[i % len(BOOK_EMOJIS)]
        buttons.append([InlineKeyboardButton(
            text=f"{emoji} {filename_to_title(f)}",
            callback_data=f"dlb_{safe(f)}"
        )])
    if not buttons:
        buttons.append([InlineKeyboardButton(text="📭 Hozircha kitob yo'q", callback_data="no_file")])
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def audio_keyboard() -> InlineKeyboardMarkup:
    files = get_files(AUDIO_DIR, AUDIO_EXTENSIONS)
    buttons = []
    for f in files:
        buttons.append([InlineKeyboardButton(
            text=f"🎙️ {filename_to_title(f)}",
            callback_data=f"dla_{safe(f)}"
        )])
    if not buttons:
        buttons.append([InlineKeyboardButton(text="📭 Hozircha audio yo'q", callback_data="no_file")])
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ── Kitoblar ──────────────────────────────────────
@router.message(F.text == "📚 Kitoblar")
async def show_books(message: Message):
    pdf_count = len(get_files(BOOKS_DIR, BOOK_EXTENSIONS))
    txt_count = len(get_files(BOOKS_DIR, AI_EXTENSIONS))
    await message.answer(
        f"📚 *G'AFUR G'ULOM KITOBLARI*\n\n"
        f"📄 Yuklab olish uchun: *{pdf_count} ta* (PDF)\n"
        "PDF kitobni tanlang 👇",
        reply_markup=books_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("dlb_"))
async def download_book(callback: CallbackQuery):
    safe_name = callback.data[4:]
    filename = find_file(safe_name, BOOKS_DIR, BOOK_EXTENSIONS)
    if not filename:
        await callback.answer("❌ Fayl topilmadi!", show_alert=True)
        return

    title = filename_to_title(filename)
    path = os.path.join(BOOKS_DIR, filename)
    await callback.answer()
    await callback.message.answer(f"📥 *{title}* yuklanmoqda...", parse_mode="Markdown")
    try:
        doc = FSInputFile(path, filename=filename)
        await callback.message.answer_document(
            document=doc,
            caption=f"📖 *{title}*\n✍️ G'afur G'ulom\n\nYoqimli mutolaa! 📚",
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.answer(
            f"❌ Yuborishda xato: {str(e)}\n\n"
            "🌐 [Ziyouz.com](https://ziyouz.com) dan ham o'qishingiz mumkin.",
            parse_mode="Markdown"
        )

# ── Audio ─────────────────────────────────────────
@router.message(F.text == "🎧 Audio hikoyalar")
async def show_audio(message: Message):
    count = len(get_files(AUDIO_DIR, AUDIO_EXTENSIONS))
    await message.answer(
        f"🎧 *G'AFUR G'ULOM AUDIO ASARLARI*\n\n"
        f"Jami: *{count} ta* audio mavjud 👇",
        reply_markup=audio_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("dla_"))
async def download_audio(callback: CallbackQuery):
    safe_name = callback.data[4:]
    filename = find_file(safe_name, AUDIO_DIR, AUDIO_EXTENSIONS)
    if not filename:
        await callback.answer("❌ Audio topilmadi!", show_alert=True)
        return

    title = filename_to_title(filename)
    path = os.path.join(AUDIO_DIR, filename)
    await callback.answer()
    await callback.message.answer(f"🎵 *{title}* yuklanmoqda...", parse_mode="Markdown")
    try:
        af = FSInputFile(path, filename=filename)
        await callback.message.answer_audio(
            audio=af,
            caption=f"🎙️ *{title}*\n✍️ G'afur G'ulom\n\nYoqimli mutolaa! 🎧",
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.answer(f"❌ Yuborishda xato: {str(e)}")

# ── Asarlar haqida ────────────────────────────────
@router.message(F.text == "📖 Asarlari haqida")
async def show_works_info(message: Message):
    from keyboards import works_menu
    await message.answer(NOVELS_INFO, reply_markup=works_menu(), parse_mode="Markdown")

@router.callback_query(F.data.startswith("works_"))
async def handle_works(callback: CallbackQuery):
    from data.gafur_data import POEMS_INFO, STORIES_INFO, NOVELS_INFO, DRAMA_INFO
    works_map = {
        "works_poems": POEMS_INFO,
        "works_stories": STORIES_INFO,
        "works_novels": NOVELS_INFO,
        "works_drama": DRAMA_INFO,
    }
    if callback.data == "works_ai_analysis":
        await callback.message.answer(
            "🤖 *'AI bilan suhbat'* tugmasini bosing!\n\nMisol: *Shum bola asarini tahlil qil*",
            parse_mode="Markdown", reply_markup=main_menu()
        )
    elif callback.data in works_map:
        await callback.message.answer(works_map[callback.data], parse_mode="Markdown")
    await callback.answer()

# ── Misc ──────────────────────────────────────────
@router.callback_query(F.data == "no_file")
async def no_file(callback: CallbackQuery):
    await callback.answer("Hozircha fayl qo'shilmagan!", show_alert=True)

@router.message(F.document)
async def receive_document(message: Message):
    fname = message.document.file_name or "fayl"
    await message.answer(
        f"📄 *{fname}* qabul qilindi!\nBot egasiga yuborildi. Rahmat! 🙏",
        parse_mode="Markdown", reply_markup=main_menu()
    )
