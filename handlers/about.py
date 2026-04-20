import os
import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import main_menu
from data.gafur_data import BIOGRAPHY

router = Router()

BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")
JSON_PATH = os.path.join(BOOKS_DIR, "gafur_data.json")

def load_json() -> dict:
    if not os.path.exists(JSON_PATH):
        return {}
    for enc in ["utf-8", "utf-8-sig"]:
        try:
            with open(JSON_PATH, "r", encoding=enc) as f:
                return json.load(f)
        except Exception:
            continue
    return {}

def get_poems_from_json() -> list:
    """JSON dan she'rlar ro'yxatini olish"""
    data = load_json()
    sherlar = data.get("ijodi", {}).get("she_riyati", {}).get("mashhur_she_rlar", [])
    return sherlar

def get_poem_content(poem: dict) -> str:
    """She'r haqida to'liq ma'lumot"""
    nom = poem.get("nom", "")
    yil = poem.get("yil", "")
    mavzu = poem.get("mavzu", "")
    izoh = poem.get("izoh", "")
    xarakter = poem.get("xarakter", "")
    sabab = poem.get("sabab", "")
    tasiri = poem.get("tasiri", "")

    text = f"🌟 *{nom}*"
    if yil:
        text += f" ({yil})"
    text += "\n_G'afur G'ulom_\n\n"
    if mavzu:
        text += f"📝 *Mavzusi:* {mavzu}\n\n"
    if sabab:
        text += f"💡 *Yozilish sababi:* {sabab}\n\n"
    if izoh:
        text += f"ℹ️ {izoh}\n\n"
    if xarakter:
        text += f"🎭 *Xarakteri:* {xarakter}\n\n"
    if tasiri:
        text += f"🌍 *Ta'siri:* {tasiri}\n\n"

    # Qo'shimcha ma'lumotlar
    extras = []
    for key, val in poem.items():
        if key not in ["nom", "yil", "mavzu", "izoh", "xarakter", "sabab", "tasiri", "nashr"] and val:
            label = key.replace("_", " ").replace("bahosi", "bahosi").title()
            extras.append(f"_{label}: {val}_")
    if extras:
        text += "\n".join(extras)

    return text

def build_poems_keyboard(sherlar: list) -> InlineKeyboardMarkup:
    """She'rlar ro'yxatidan klaviatura yaratish"""
    buttons = []
    for i, sh in enumerate(sherlar[:20]):  # Max 20 ta
        nom = sh.get("nom", f"She'r {i+1}")
        # Nomni qisqartirish (30 belgi)
        short_nom = nom[:30] + "..." if len(nom) > 30 else nom
        buttons.append([InlineKeyboardButton(
            text=f"📜 {short_nom}",
            callback_data=f"poem_{i}"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ═══════════════════════════════════════
# HANDLERS
# ═══════════════════════════════════════

@router.message(F.text == "ℹ️ Tarjimayi hol")
async def cmd_bio(message: Message):
    data = load_json()
    if data:
        s = data.get("shaxs", {})
        joy = s.get("tug_ilgan_joy", {})
        unvonlar = "\n".join([f"• {u}" for u in s.get("unvonlar", [])])
        mukofotlar = "\n".join([
            f"• {m.get('nom','')} {m.get('yil','')}"
            for m in s.get("mukofotlar", [])
        ])
        bio = (
            f"👤 *G'AFUR G'ULOM*\n\n"
            f"📛 *To'liq ismi:* {s.get('asl_ismi','')}\n"
            f"📅 *Tug'ilgan:* {s.get('tug_ilgan_sana','')}\n"
            f"📍 *Joy:* {joy.get('shahar','')}, {joy.get('mahalla','')}\n"
            f"⚰️ *Vafot:* {s.get('vafot_sana','')} ({s.get('vafot_yoshi','')} yoshida)\n"
            f"🏛️ *Dafn:* {s.get('dafn_etilgan','')}\n\n"
            f"🏆 *Unvonlari:*\n{unvonlar}\n\n"
            f"🎖️ *Mukofotlari:*\n{mukofotlar}"
        )
        await message.answer(bio, parse_mode="Markdown", reply_markup=main_menu())
    else:
        await message.answer(BIOGRAPHY, parse_mode="Markdown", reply_markup=main_menu())

@router.message(F.text == "🎭 She'rlar")
async def show_poems(message: Message):
    sherlar = get_poems_from_json()
    if sherlar:
        keyboard = build_poems_keyboard(sherlar)
        await message.answer(
            f"🎭 *G'AFUR G'ULOM SHE'RLARI*\n\n"
            f"Jami: *{len(sherlar)} ta* mashhur she'r\n"
            f"She'r tanlang 👇",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        # JSON yo'q — standart menyu
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📜 Sen yetim emassan", callback_data="poem_static_1")],
            [InlineKeyboardButton(text="📜 Sog'inish", callback_data="poem_static_2")],
            [InlineKeyboardButton(text="📜 Vaqt", callback_data="poem_static_3")],
            [InlineKeyboardButton(text="📜 Men yahudiyman", callback_data="poem_static_4")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
        ])
        await message.answer(
            "🎭 *G'AFUR G'ULOM SHE'RLARI*\n\nShe'r tanlang 👇",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

@router.callback_query(F.data.startswith("poem_"))
async def show_poem(callback: CallbackQuery):
    data_part = callback.data[5:]  # "poem_" dan keyingi qism

    if data_part.startswith("static_"):
        # Statik she'rlar
        static = {
            "1": "🌟 *Sen yetim emassan* (1942)\n\n1942-yilda urush paytida yozilgan. Yetim bolalarga bag'ishlangan.",
            "2": "🌟 *Sog'inish* (1942)\n\nO'g'lini frontga kuzatgan otaning dardi haqida.",
            "3": "🌟 *Vaqt* (1945)\n\nVaqtning qadri va inson umri haqida falsafiy she'r.",
            "4": "🌟 *Men yahudiyman* (1941)\n\nFashizmga qarshi, xalqlar do'stligi haqida.",
        }
        num = data_part.replace("static_", "")
        text = static.get(num, "❌ Topilmadi")
        await callback.message.answer(text, parse_mode="Markdown")
    else:
        # JSON dan
        try:
            idx = int(data_part)
            sherlar = get_poems_from_json()
            if 0 <= idx < len(sherlar):
                text = get_poem_content(sherlar[idx])
                await callback.message.answer(text, parse_mode="Markdown")
            else:
                await callback.message.answer("❌ She'r topilmadi.")
        except (ValueError, IndexError):
            await callback.message.answer("❌ Xato yuz berdi.")

    await callback.answer()

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.answer("Asosiy menyu:", reply_markup=main_menu())
    await callback.answer()

@router.message(F.text & ~F.text.startswith("/"))
async def handle_general(message: Message):
    skip = [
        "📚 Kitoblar", "🎧 Audio hikoyalar", "📖 Asarlari haqida",
        "ℹ️ Tarjimayi hol", "🎭 She'rlar", "❓ Yordam", "🔍 Qidirish"
    ]
    if message.text in skip:
        return
    await message.answer(
        "💡 Menyudan tanlang yoki *🔍 Qidirish* tugmasini bosing.",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )
