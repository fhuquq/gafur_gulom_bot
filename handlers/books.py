import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import main_menu
from data.gafur_data import NOVELS_INFO

router = Router()

# Kitoblar va audiolar katalogi
BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "audio")
# Bu yerga audio fayl nomi va uni o'qigan diktor ismini yozasiz
AUDIO_READERS = {
    "Shum_bola": "Anvar Alimov",
    "Netay": "Zulfiya",
    "Yodgor": "Afzal Rafiqov"
}
BOOK_EMOJIS = ["📗", "📘", "📙", "📕", "📓", "📒", "📔", "📖"]

def get_files_from_dir(directory: str, extensions: list) -> list:
    """Papkadagi fayllarni avtomatik topish"""
    if not os.path.exists(directory):
        return []
    files = []
    for f in sorted(os.listdir(directory)):
        if any(f.lower().endswith(ext) for ext in extensions):
            files.append(f)
    return files

def filename_to_title(filename: str) -> str:
    """Fayl nomini chiroyli sarlavhaga aylantirish"""
    name = os.path.splitext(filename)[0]  # kengaytmasiz nom
    # _ va - ni bo'shliqqa almashtirish
    name = name.replace("_", " ").replace("-", " ")
    # Har so'zni bosh harf bilan
    return name.title()

def build_books_keyboard() -> InlineKeyboardMarkup:
    """Papkadagi kitoblar asosida klaviatura yaratish"""
    files = get_files_from_dir(BOOKS_DIR, [".pdf", ".epub", ".docx"])
    buttons = []
    for i, filename in enumerate(files):
        title = filename_to_title(filename)
        emoji = BOOK_EMOJIS[i % len(BOOK_EMOJIS)]
        safe_name = filename.replace(".", "_").replace(" ", "__")
        buttons.append([InlineKeyboardButton(
            text=f"{emoji} {title}",
            callback_data=f"dl_book_{safe_name}"
        )])
    if not buttons:
        buttons.append([InlineKeyboardButton(
            text="📭 Hozircha kitob yo'q",
            callback_data="no_books"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def build_audio_keyboard() -> InlineKeyboardMarkup:
    """Papkadagi audiolar asosida klaviatura yaratish"""
    files = get_files_from_dir(AUDIO_DIR, [".mp3", ".ogg", ".m4a", ".wav"])
    buttons = []
    for filename in files:
        title = filename_to_title(filename)
        safe_name = filename.replace(".", "_").replace(" ", "__")
        buttons.append([InlineKeyboardButton(
            text=f"🎙️ {title}",
            callback_data=f"dl_audio_{safe_name}"
        )])
    if not buttons:
        buttons.append([InlineKeyboardButton(
            text="📭 Hozircha audio yo'q",
            callback_data="no_audio"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def safe_name_to_filename(safe_name: str, directory: str, extensions: list) -> str | None:
    """safe_name dan asl fayl nomini tiklash"""
    files = get_files_from_dir(directory, extensions)
    for filename in files:
        converted = filename.replace(".", "_").replace(" ", "__")
        if converted == safe_name:
            return filename
    return None

@router.message(F.text == "📚 Kitoblar")
async def show_books(message: Message):
    files = get_files_from_dir(BOOKS_DIR, [".pdf", ".epub", ".docx"])
    count = len(files)
    await message.answer(
        f"📚 *G'AFUR G'ULOM KITOBLARI*\n\n"
        f"Jami: *{count} ta* kitob mavjud\n"
        f"PDF formatda yuklab olishingiz mumkin 👇",
        reply_markup=build_books_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text == "🎧 Audio hikoyalar")
async def show_audio(message: Message):
    files = get_files_from_dir(AUDIO_DIR, [".mp3", ".ogg", ".m4a", ".wav"])
    count = len(files)
    await message.answer(
        f"🎧 *G'AFUR G'ULOM AUDIO ASARLARI*\n\n"
        f"Jami: *{count} ta* audio mavjud\n"
        f"MP3 formatda yuklab olishingiz mumkin 👇",
        reply_markup=build_audio_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text == "📖 Asarlari haqida")
async def show_works_info(message: Message):
    from keyboards import works_menu
    await message.answer(
        NOVELS_INFO,
        reply_markup=works_menu(),
        parse_mode="Markdown"
    )

# Kitob yuklab olish
@router.callback_query(F.data.startswith("dl_book_"))
async def download_book(callback: CallbackQuery):
    safe_name = callback.data[len("dl_book_"):]
    filename = safe_name_to_filename(safe_name, BOOKS_DIR, [".pdf", ".epub", ".docx"])

    if not filename:
        await callback.answer("❌ Fayl topilmadi!", show_alert=True)
        return

    title = filename_to_title(filename)
    book_path = os.path.join(BOOKS_DIR, filename)

    await callback.answer()
    await callback.message.answer(f"📥 *{title}* yuklanmoqda...", parse_mode="Markdown")

    try:
        doc = FSInputFile(book_path, filename=filename)
        await callback.message.answer_document(
            document=doc,
            caption=f"📖 *{title}*\n✍️ G'afur G'ulom\n\nYoqimli mutolaa! 📚",
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.answer(
            f"❌ Faylni yuborishda xato: {str(e)}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🌐 Ziyouz.com", url="https://ziyouz.com")],
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
            ])
        )

@router.callback_query(F.data.startswith("dl_audio_"))
async def download_audio(callback: CallbackQuery):
    safe_name = callback.data[len("dl_audio_"):]
    filename = safe_name_to_filename(safe_name, AUDIO_DIR, [".mp3", ".ogg", ".m4a", ".wav"])

    if not filename:
        await callback.answer("❌ Audio topilmadi!", show_alert=True)
        return

    title = filename_to_title(filename)
    audio_path = os.path.join(AUDIO_DIR, filename)
    
    # Diktor ismini lug'atdan qidirish
    file_key = os.path.splitext(filename)[0]
    reader_name = AUDIO_READERS.get(file_key, "G'afur G'ulom (o'z ijrolari)")

    await callback.answer()
    await callback.message.answer(f"🎵 *{title}* yuklanmoqda...", parse_mode="Markdown")

    try:
        audio_file = FSInputFile(audio_path, filename=filename)
        await callback.message.answer_audio(
            audio=audio_file,
            caption=(
                f"🎙️ *{title}*\n"
                f"✍️ Muallif: G'afur G'ulom\n"
                f"📖 O'qigan: {reader_name}\n\n"
                f"Yaxshi tinglashlar! 🎧"
            ),
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.answer(f"❌ Faylni yuborishda xato: {str(e)}")

# Works callbacks
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
            "🤖 AI tahlil uchun *'AI bilan suhbat'* tugmasini bosing!\n\n"
            "Misol: *'Shum bola asarini tahlil qil'*",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    elif callback.data in works_map:
        await callback.message.answer(works_map[callback.data], parse_mode="Markdown")
    await callback.answer()

# Foydalanuvchi fayl yuborsa — qabul qilish
@router.message(F.document)
async def receive_document(message: Message):
    fname = message.document.file_name or "fayl"
    await message.answer(
        f"📄 *{fname}* qabul qilindi!\n\n"
        "Bu fayl bot egasiga yuborildi. Tekshirilgandan so'ng serverga qo'shiladi. Rahmat! 🙏",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )
