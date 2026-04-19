from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from keyboards import main_menu
from data.gafur_data import BIOGRAPHY

router = Router()

WELCOME_TEXT = """
🌟 *Assalomu alaykum!*

*G'AFUR G'ULOM BOTiga xush kelibsiz!*

Men sizga buyuk o'zbek shoiri va yozuvchisi *G'afur G'ulom* (1903-1966) haqida har qanday ma'lumot bera olaman.

*Nima qila olaman:*
🤖 *AI suhbat* — Istalgan savolingizga javob beraman
📚 *Kitoblar* — Elektron asarlarni yuklab olish
🎧 *Audio* — Hikoya va she'rlarni tinglash
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

*Qo'shimcha:*
• Istalgan savolingizni yozsangiz, AI javob beradi
• Kitob yoki audio so'rasangiz, yuboriladi
• "AI bilan suhbat" tugmasini bosib, chuqur suhbat boshlang

📞 *Muammo bo'lsa:* @admin ga yozing
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
