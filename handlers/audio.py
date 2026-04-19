from aiogram import Router, F
from aiogram.types import Message
from keyboards import main_menu

router = Router()

# Audio va kitoblar endi handlers/books.py da boshqariladi
# Bu fayl faqat audio xabarlarni qabul qilish uchun

@router.message(F.audio | F.voice)
async def receive_audio(message: Message):
    file = message.audio or message.voice
    file_name = getattr(message.audio, 'file_name', 'audio.ogg') if message.audio else 'voice.ogg'
    size_kb = file.file_size // 1024

    await message.answer(
        f"🎵 *Audio qabul qilindi!*\n\n"
        f"📁 Fayl: `{file_name}`\n"
        f"📦 Hajm: {size_kb} KB\n\n"
        "Bot egasiga yuborildi. Tekshirilgandan so'ng serverga qo'shiladi.\n"
        "Rahmat! 🙏",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

