import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import main_menu, audio_menu

router = Router()

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "audio")

AUDIO_DATA = {
    "audio_shum_bola": {
        "title": "🎙️ Shum bola (audiokitob)",
        "description": "G'afur G'ulomning 'Shum bola' asari audio formatda",
        "filename": "shum_bola_audio.mp3",
        "duration": "~2 soat"
    },
    "audio_sherlar": {
        "title": "🎙️ She'rlar to'plami",
        "description": "G'afur G'ulomning mashhur she'rlari",
        "filename": "sherlar.mp3",
        "duration": "~45 daqiqa"
    },
    "audio_hikoyalar": {
        "title": "🎙️ Hikoyalar",
        "description": "G'afur G'ulom hikoyalari audio formatda",
        "filename": "hikoyalar.mp3",
        "duration": "~1 soat"
    },
    "audio_full": {
        "title": "🎙️ To'liq asarlar (audio)",
        "description": "Barcha audio asarlar to'plami",
        "filename": "full_audio.mp3",
        "duration": "~5 soat"
    }
}

@router.message(F.text == "🎧 Audio hikoyalar")
async def show_audio(message: Message):
    await message.answer(
        "🎧 *G'AFUR G'ULOM AUDIO ASARLARI*\n\n"
        "Audio formatdagi asarlardan birini tanlang.\n"
        "MP3 formatida yuklab olishingiz mumkin:",
        reply_markup=audio_menu(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("audio_"))
async def handle_audio_selection(callback: CallbackQuery):
    audio_key = callback.data
    
    if audio_key not in AUDIO_DATA:
        await callback.answer("❌ Audio topilmadi!")
        return
    
    audio = AUDIO_DATA[audio_key]
    audio_path = os.path.join(AUDIO_DIR, audio["filename"])
    
    # Audio ma'lumotlarini yuborish
    await callback.message.answer(
        f"🎙️ *{audio['title']}*\n\n"
        f"📝 {audio['description']}\n"
        f"⏱️ *Davomiylik:* {audio['duration']}",
        parse_mode="Markdown"
    )
    
    # Fayl mavjudligini tekshirish
    if os.path.exists(audio_path):
        try:
            audio_file = FSInputFile(audio_path, filename=audio["filename"])
            await callback.message.answer_audio(
                audio=audio_file,
                caption=f"🎵 *{audio['title']}*\n\nYaxshi tinglashlar! 🎧",
                parse_mode="Markdown"
            )
        except Exception as e:
            await send_audio_not_available(callback.message, audio["title"])
    else:
        await send_audio_not_available(callback.message, audio["title"])
    
    await callback.answer()

async def send_audio_not_available(message, audio_title: str):
    """Audio mavjud bo'lmasa yo'nalish ko'rsatish"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🎵 YouTube da tinglash",
                url="https://www.youtube.com/results?search_query=G%27afur+G%27ulom+audiokitob"
            )],
            [InlineKeyboardButton(
                text="📻 Ziyouz audio",
                url="https://ziyouz.com"
            )],
            [InlineKeyboardButton(text="🔙 Audio menyu", callback_data="back_audio")]
        ]
    )
    
    await message.answer(
        f"⚠️ *{audio_title}*\n\n"
        "Bu audio hozirda bot serverida mavjud emas.\n\n"
        "📌 *Audio topish uchun:*\n"
        "• YouTube: 'G'afur G'ulom audiokitob'\n"
        "• Ziyouz.com\n"
        "• Spotify: G'afur G'ulom\n\n"
        "💡 *Agar sizda audio fayllar bo'lsa, bot egasiga yuboring — serverga qo'shiladi!*\n\n"
        "📤 *Audio faylni to'g'ridan-to'g'ri botga yuborishingiz mumkin!*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "back_audio")
async def back_to_audio(callback: CallbackQuery):
    await callback.message.answer("🎧 Audio:", reply_markup=audio_menu())
    await callback.answer()

# Foydalanuvchi audio yuborsa — saqlab olish
@router.message(F.audio | F.voice)
async def receive_audio(message: Message):
    file = message.audio or message.voice
    file_name = getattr(message.audio, 'file_name', 'audio_file.ogg') if message.audio else 'voice.ogg'
    
    await message.answer(
        f"🎵 *Audio qabul qilindi!*\n\n"
        f"📁 Fayl: `{file_name}`\n"
        f"📦 Hajm: {file.file_size // 1024} KB\n\n"
        "Bu audio bot egasiga yuborildi. Tekshirilgandan so'ng serverga qo'shiladi.\n\n"
        "Rahmat! 🙏",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )
