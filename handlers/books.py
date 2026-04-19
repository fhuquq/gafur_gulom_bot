import os
import aiofiles
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import main_menu, books_menu
from data.gafur_data import NOVELS_INFO

router = Router()

# Kitoblar katalogi
BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")

# Kitoblar ma'lumotlari
BOOKS_DATA = {
    "book_shum_bola": {
        "title": "📗 Shum bola",
        "author": "G'afur G'ulom",
        "year": "1936",
        "description": (
            "*\"Shum bola\"* — G'afur G'ulomning eng mashhur avtobiografik qissasi.\n\n"
            "Asar 1900-1910-yillarda Toshkentda o'sgan bolaning hayotini tasvirlaydi. "
            "Yozuvchi o'z bolaligini hazilomuz, samimiy til bilan hikoya qiladi.\n\n"
            "*Asosiy mavzular:* Bolalik, yetimlik, do'stlik, hayotga muhabbat\n"
            "*Janr:* Avtobiografik qissa\n"
            "*Hajm:* ~200 bet"
        ),
        "filename": "shum_bola.pdf"
    },
    "book_ogrigina": {
        "title": "📘 Mening o'g'rigina bolam",
        "author": "G'afur G'ulom",
        "year": "1963",
        "description": (
            "*\"Mening o'g'rigina bolam\"* — bolalar tarbiyasi va ota-ona muhabbati haqidagi qissa.\n\n"
            "*Janr:* Qissa\n"
            "*Yil:* 1963"
        ),
        "filename": "ogrigina_bolam.pdf"
    },
    "book_kucha": {
        "title": "📙 Ko'cha bolasi",
        "author": "G'afur G'ulom",
        "year": "1935",
        "description": (
            "*\"Ko'cha bolasi\"* — Toshkent ko'chalarida o'sayotgan bola haqida.\n\n"
            "*Janr:* Qissa"
        ),
        "filename": "kucha_bolasi.pdf"
    },
    "book_sariq_devlar": {
        "title": "📕 Sariq devlar",
        "author": "G'afur G'ulom",
        "year": "1958",
        "description": (
            "*\"Sariq devlar\"* — mustamlakachilik davriga bag'ishlangan roman.\n\n"
            "*Janr:* Roman\n"
            "*Yil:* 1958"
        ),
        "filename": "sariq_devlar.pdf"
    },
    "book_navoiy": {
        "title": "📓 Navoiy",
        "author": "G'afur G'ulom",
        "year": "1944",
        "description": (
            "*\"Navoiy\"* — Alisher Navoiy hayotiga bag'ishlangan tarixiy roman.\n\n"
            "Bu asar uchun G'afur G'ulom 1946-yilda Stalin mukofotiga sazovor bo'lgan.\n\n"
            "*Janr:* Tarixiy roman\n"
            "*Yil:* 1944"
        ),
        "filename": "navoiy.pdf"
    },
    "book_tola": {
        "title": "📒 To'la asarlar to'plami",
        "author": "G'afur G'ulom",
        "year": "1970s",
        "description": (
            "*G'afur G'ulomning to'la asarlar to'plami*\n\n"
            "She'rlar, hikoyalar, qissalar va romanlari yig'ilgan to'plam.\n\n"
            "*Janr:* To'plam"
        ),
        "filename": "tola_asarlar.pdf"
    }
}

@router.message(F.text == "📚 Kitoblar")
async def show_books(message: Message):
    await message.answer(
        "📚 *G'AFUR G'ULOM ASARLARI*\n\n"
        "Quyidagi asarlardan birini tanlang.\n"
        "PDF formatda yuklab olishingiz mumkin:",
        reply_markup=books_menu(),
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

@router.callback_query(F.data.startswith("book_"))
async def handle_book_selection(callback: CallbackQuery):
    book_key = callback.data
    
    if book_key not in BOOKS_DATA:
        await callback.answer("❌ Kitob topilmadi!")
        return
    
    book = BOOKS_DATA[book_key]
    book_path = os.path.join(BOOKS_DIR, book["filename"])
    
    # Kitob ma'lumotlarini yuborish
    info_text = (
        f"{book['title']}\n"
        f"✍️ *Muallif:* {book['author']}\n"
        f"📅 *Yil:* {book['year']}\n\n"
        f"{book['description']}"
    )
    
    await callback.message.answer(info_text, parse_mode="Markdown")
    
    # Fayl mavjudligini tekshirish
    if os.path.exists(book_path):
        try:
            document = FSInputFile(book_path, filename=book["filename"])
            await callback.message.answer_document(
                document=document,
                caption=f"📥 *{book['title']}* — yuklab olindi!\n\nYaxshi o'qishlar! 📖",
                parse_mode="Markdown"
            )
        except Exception as e:
            await send_book_not_available(callback.message, book["title"])
    else:
        await send_book_not_available(callback.message, book["title"])
    
    await callback.answer()

async def send_book_not_available(message, book_title: str):
    """Kitob mavjud bo'lmasa alternativ yo'nalish ko'rsatish"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🌐 Ziyouz.com da o'qish",
                url="https://ziyouz.com/o%CA%BBzbek-nasri/gafur-gulom/"
            )],
            [InlineKeyboardButton(
                text="📖 EKitob.uz da o'qish",
                url="https://ekitob.uz"
            )],
            [InlineKeyboardButton(text="🔙 Kitoblar", callback_data="back_books")]
        ]
    )
    
    await message.answer(
        f"⚠️ *{book_title}*\n\n"
        "Hozirda bu kitob bot serverida mavjud emas.\n\n"
        "📌 *Kitobni quyidagi manbalardan toping:*\n"
        "• Ziyouz.com — O'zbek kitoblar kutubxonasi\n"
        "• EKitob.uz — Elektron kitoblar\n"
        "• Milliy kutubxona.uz\n\n"
        "💡 *Bot egasiga kitob fayllarini yuborish mumkin — u serverga qo'shadi!*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "back_books")
async def back_to_books(callback: CallbackQuery):
    await callback.message.answer("📚 Kitoblar:", reply_markup=books_menu())
    await callback.answer()

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
            "🤖 AI tahlil uchun *'AI bilan suhbat'* tugmasini bosing va savolingizni yozing!\n\n"
            "Misol: *'Shum bola asarini tahlil qil'*",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    elif callback.data in works_map:
        await callback.message.answer(
            works_map[callback.data],
            parse_mode="Markdown"
        )
    
    await callback.answer()
