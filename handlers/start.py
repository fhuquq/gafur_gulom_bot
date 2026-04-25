from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from keyboards import main_menu
from data.gafur_data import BIOGRAPHY

router = Router()

WELCOME_TEXT = """
🌟 *Assalomu alaykum!*

*G'AFUR G'ULOM HAYOTI VA IJODINI YORITUVCHI BOTGA XUSH KELIBSIZ!*

Men sizga buyuk o'zbek shoiri va yozuvchisi *G'afur G'ulom* (1903-1966) haqida har qanday ma'lumot bera olaman.

*Nima qila olaman:*
🤖 *Testlar* — Adibning hayoti va ijodini qanchalik bilasiz? Sinab ko'ring!
📚 *Kitoblar* — Elektron asarlarni yuklab oling
🎧 *Audio* — Hikoya va she'rlarni tinglang
📖 *Asarlar* — Barcha asarlari haqida ma'lumot
ℹ️ *Tarjimayi hol* — Hayot yo'li

Quyidagi menyudan tanlang yoki to'g'ridan-to'g'ri savol yozing! 👇
"""

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@router.message(Command("help"))
@router.message(F.text == "❓ Yordam")
async def cmd_help(message: Message):
    help_text = """
❓ *YORDAM — BOT BUYRUQLARI*

*/start* — Botni qayta ishga tushirish
*/help* — Yordam
*/bio* — G'afur G'ulom tarjimayi holi
*/poems* — She'rlar ro'yxati
*/stories* — Hikoyalar
*/books* — Kitoblar

📞 *Muammo bo'lsa:* @UsmonovIbrohim ga yozing
    """
    await message.answer(help_text, parse_mode="Markdown", reply_markup=main_menu())

@router.message(Command("bio"))
@router.message(F.text == "ℹ️ Tarjimayi hol")
async def cmd_bio(message: Message):
    await message.answer(BIOGRAPHY, parse_mode="Markdown", reply_markup=main_menu())

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer("Asosiy menyu:", reply_markup=main_menu())
    await callback.answer()
