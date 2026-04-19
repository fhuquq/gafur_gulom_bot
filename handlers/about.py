from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import main_menu
from data.gafur_data import POEMS_INFO, STORIES_INFO, BIOGRAPHY
from handlers.ai_chat import ask_claude

router = Router()

FAMOUS_POEMS = {
    "sen_yetim": {
        "title": "🌟 Sen yetim emassan",
        "text": (
            "*\"SEN YETIM EMASSAN\"*\n"
            "_G'afur G'ulom_\n\n"
            "_(1942-yil, Urush davri she'ri)_\n\n"
            "Bu she'r 1942-yilda Ikkinchi Jahon urushi paytida yozilgan. "
            "Urushda ota-onasini yo'qotgan bolalarga bag'ishlangan bu she'r "
            "o'zbek adabiyotining eng ta'sirchan asarlaridan biri hisoblanadi.\n\n"
            "🤖 *She'r tahlili uchun 'AI bilan suhbat' bo'limiga o'ting.*"
        )
    },
    "asrlar": {
        "title": "🌟 Asrlar mening ota-bobolarim",
        "text": (
            "*\"ASRLAR MENING OTA-BOBOLARIM\"*\n"
            "_G'afur G'ulom_\n\n"
            "Bu she'rda shoir o'zbek xalqining boy tarixi va madaniyatiga murojaat qiladi. "
            "O'tmish va bugungi kun o'rtasidagi bog'liqlik, ajdodlarga ehtirom — "
            "asarning asosiy mavzulari.\n\n"
            "🤖 *She'r tahlili uchun 'AI bilan suhbat' bo'limiga o'ting.*"
        )
    }
}

@router.message(F.text == "🎭 She'rlar")
async def show_poems(message: Message):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📜 Sen yetim emassan", callback_data="poem_sen_yetim")],
            [InlineKeyboardButton(text="📜 Asrlar mening ota-bobolarim", callback_data="poem_asrlar")],
            [InlineKeyboardButton(text="📜 Toshkentim", callback_data="poem_toshkent")],
            [InlineKeyboardButton(text="📜 Yoshlik", callback_data="poem_yoshlik")],
            [InlineKeyboardButton(text="🤖 AI dan she'r tahlili so'rash", callback_data="poem_ai_analysis")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
        ]
    )
    
    await message.answer(
        "🎭 *G'AFUR G'ULOM SHE'RLARI*\n\n"
        "She'rlar ro'yxatidan birini tanlang\n"
        "yoki AI dan she'r tahlili so'rang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("poem_"))
async def handle_poem(callback: CallbackQuery):
    poem_key = callback.data.replace("poem_", "")
    
    if poem_key == "ai_analysis":
        await callback.message.answer(
            "🤖 *She'r tahlili*\n\n"
            "'AI bilan suhbat' tugmasini bosing va:\n"
            "`Sen yetim emassan she'rini tahlil qil`\n"
            "deb yozing!",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        await callback.answer()
        return
    
    if poem_key == "toshkent":
        text = (
            "*\"TOSHKENTIM\"*\n"
            "_G'afur G'ulom_\n\n"
            "Ona shahri Toshkentga bag'ishlangan lirik she'r. "
            "Shoir Toshkentning go'zalligi, uning tarixi va kelajagi haqida samimiy his-tuyg'ularini bayon etadi.\n\n"
            "🤖 *Batafsil tahlil uchun AI bilan suhbatlashing.*"
        )
    elif poem_key == "yoshlik":
        text = (
            "*\"YOSHLIK\"*\n"
            "_G'afur G'ulom_\n\n"
            "Yoshlik davri haqidagi lirik she'r. "
            "Shoir yoshlik vaqtining qadri va uning o'tib ketishi haqida fikr yuritadi.\n\n"
            "🤖 *Batafsil tahlil uchun AI bilan suhbatlashing.*"
        )
    elif poem_key in ["sen_yetim", "asrlar"]:
        poem_data = FAMOUS_POEMS.get(poem_key)
        text = poem_data["text"] if poem_data else "She'r topilmadi."
    else:
        text = "❌ Bu she'r hozircha mavjud emas."
    
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

# Umumiy matn xabarlari — AI ga yo'naltirish (oxirgi handler)
@router.message(F.text & ~F.text.startswith("/"))
async def handle_general_text(message: Message):
    """Oddiy matn xabarlarini AI ga yuborish"""
    text = message.text.lower()
    
    # Maxsus kalit so'zlar bo'lmasa, AI ga yuborish
    skip_words = [
        "🤖 ai bilan suhbat", "📚 kitoblar", "🎧 audio hikoyalar",
        "📖 asarlari haqida", "ℹ️ tarjimayi hol", "🎭 she'rlar", "❓ yordam"
    ]
    
    if message.text in skip_words:
        return
    
    # AI ga yuborish
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
        await message.answer(
            "❌ Xato yuz berdi. Qayta urinib ko'ring.\n"
            "Yoki *'AI bilan suhbat'* tugmasini bosing.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
