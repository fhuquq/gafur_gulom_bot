import os
import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import main_menu
from data.gafur_data import POEMS_INFO, STORIES_INFO, BIOGRAPHY

router = Router()

BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")

def load_texts() -> dict:
    result = {}
    if not os.path.exists(BOOKS_DIR):
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
    return result

def search_texts(query: str, max_results: int = 4) -> list:
    texts = load_texts()
    if not texts:
        return []
    words = [w for w in re.findall(r'\w+', query.lower()) if len(w) > 2]
    if not words:
        return []
    results = []
    for title, content in texts.items():
        paragraphs = [p.strip() for p in content.split('\n') if len(p.strip()) > 30]
        for para in paragraphs:
            score = sum(1 for w in words if w in para.lower())
            if score > 0:
                results.append((score, title, para))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:max_results]

# She'rlar menyusi
POEMS_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📜 Sen yetim emassan", callback_data="poem_1")],
    [InlineKeyboardButton(text="📜 Asrlar mening ota-bobolarim", callback_data="poem_2")],
    [InlineKeyboardButton(text="📜 Toshkentim", callback_data="poem_3")],
    [InlineKeyboardButton(text="📜 Yoshlik", callback_data="poem_4")],
    [InlineKeyboardButton(text="📜 O'zbekiston", callback_data="poem_5")],
    [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
])

POEMS_CONTENT = {
    "poem_1": (
        "🌟 *SEN YETIM EMASSAN* (1942)\n"
        "_G'afur G'ulom_\n\n"
        "Bu she'r 1942-yilda Ikkinchi Jahon urushi paytida yozilgan.\n"
        "Urushda otasini yo'qotgan bolalarga bag'ishlangan.\n\n"
        "She'rning asosiy g'oyasi: urushda yetim qolgan bola yolg'iz emas,\n"
        "butun xalq uning otasi. Umid va bardosh haqidagi buyuk asar.\n\n"
        "📌 _To'liq matn TXT faylida mavjud. '🔍 Qidirish' orqali toping._"
    ),
    "poem_2": (
        "🌟 *ASRLAR MENING OTA-BOBOLARIM*\n"
        "_G'afur G'ulom_\n\n"
        "O'zbek xalqining boy tarixi va ajdodlarga ehtiromga bag'ishlangan she'r.\n"
        "Temur, Navoiy, Ulug'bek kabi buyuk ajdodlar ulug'lanadi.\n\n"
        "📌 _To'liq matn TXT faylida mavjud. '🔍 Qidirish' orqali toping._"
    ),
    "poem_3": (
        "🌟 *TOSHKENTIM*\n"
        "_G'afur G'ulom_\n\n"
        "Ona shahri Toshkentga muhabbat haqidagi lirik she'r.\n"
        "Shoir Toshkentning go'zalligi, tarixi va kelajagi haqida yozgan.\n\n"
        "📌 _To'liq matn TXT faylida mavjud. '🔍 Qidirish' orqali toping._"
    ),
    "poem_4": (
        "🌟 *YOSHLIK*\n"
        "_G'afur G'ulom_\n\n"
        "Yoshlik davri, uning qadri va o'tkinchiligi haqidagi lirik she'r.\n\n"
        "📌 _To'liq matn TXT faylida mavjud. '🔍 Qidirish' orqali toping._"
    ),
    "poem_5": (
        "🌟 *O'ZBEKISTON*\n"
        "_G'afur G'ulom_\n\n"
        "Vatan — O'zbekistonga bag'ishlangan vatanparvarlik she'ri.\n\n"
        "📌 _To'liq matn TXT faylida mavjud. '🔍 Qidirish' orqali toping._"
    ),
}

@router.message(F.text == "ℹ️ Tarjimayi hol")
async def cmd_bio(message: Message):
    # Avval TXT dan qidirish, bo'lmasa standart
    results = search_texts("tug'ilgan hayot ijod 1903", max_results=2)
    if results:
        txt_part = "\n\n".join([f"📌 _{para[:500]}_" for _, _, para in results])
        await message.answer(
            BIOGRAPHY + f"\n\n📖 *Manbadan:*\n{txt_part}",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    else:
        await message.answer(BIOGRAPHY, parse_mode="Markdown", reply_markup=main_menu())

@router.message(F.text == "🎭 She'rlar")
async def show_poems(message: Message):
    await message.answer(
        "🎭 *G'AFUR G'ULOM SHE'RLARI*\n\n"
        "She'r tanlang yoki '🔍 Qidirish' orqali she'r nomini yozing:",
        reply_markup=POEMS_KEYBOARD,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("poem_"))
async def show_poem(callback: CallbackQuery):
    content = POEMS_CONTENT.get(callback.data, "❌ Topilmadi")
    # TXT dan ham qidirish
    poem_name = content.split("*")[1] if "*" in content else ""
    if poem_name:
        results = search_texts(poem_name.lower(), max_results=2)
        if results:
            extra = "\n\n📖 *Manbadan topildi:*\n" + "\n\n".join([f"_{p[:400]}_" for _, _, p in results])
            content += extra
    await callback.message.answer(content, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.answer("Asosiy menyu:", reply_markup=main_menu())
    await callback.answer()

# Umumiy matn xabarlar — qidiruvga yo'naltirish
@router.message(F.text & ~F.text.startswith("/"))
async def handle_general(message: Message):
    skip = [
        "📚 Kitoblar", "🎧 Audio hikoyalar", "📖 Asarlari haqida",
        "ℹ️ Tarjimayi hol", "🎭 She'rlar", "❓ Yordam", "🔍 Qidirish"
    ]
    if message.text in skip:
        return

    results = search_texts(message.text, max_results=3)
    if results:
        response = f"🔍 *'{message.text}'* bo'yicha topildi:\n\n"
        for _, title, para in results:
            short = para[:400] + "..." if len(para) > 400 else para
            response += f"📌 *[{title}]*\n{short}\n\n─────────────\n\n"
        await message.answer(response, parse_mode="Markdown", reply_markup=main_menu())
    else:
        await message.answer(
            "❓ Bu haqda ma'lumot topilmadi.\n\n"
            "💡 *'🔍 Qidirish'* tugmasini bosib, kalit so'z yozing.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
