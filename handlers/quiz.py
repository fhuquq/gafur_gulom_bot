import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import main_menu
from data.tests import TESTS

router = Router()

class QuizState(StatesGroup):
    playing = State()

HARFLAR = ["A", "B", "C", "D"]

def test_keyboard(test: dict, test_idx: int) -> InlineKeyboardMarkup:
    buttons = []
    for i, variant in enumerate(test["variantlar"]):
        buttons.append([InlineKeyboardButton(
            text=f"{HARFLAR[i]}) {variant}",
            callback_data=f"quiz_ans_{test_idx}_{i}"
        )])
    buttons.append([InlineKeyboardButton(text="⏭ Keyingi savol", callback_data=f"quiz_skip_{test_idx}")])
    buttons.append([InlineKeyboardButton(text="🏁 Testni tugatish", callback_data="quiz_end")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Qayta boshlash", callback_data="quiz_restart")],
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="quiz_home")]
    ])

def format_result(score: int, total: int) -> str:
    percent = int(score / total * 100)
    if percent == 100:
        emoji = "🏆"
        baho = "Mukammal! Siz G'afur G'ulom haqida hamma narsani bilasiz!"
    elif percent >= 80:
        emoji = "🥇"
        baho = "Ajoyib natija! Siz bu buyuk shoir haqida juda ko'p bilasiz!"
    elif percent >= 60:
        emoji = "🥈"
        baho = "Yaxshi natija! Yana biroz o'rgansangiz, mukammal bo'lasiz."
    elif percent >= 40:
        emoji = "🥉"
        baho = "Qoniqarli. G'afur G'ulom asarlarini o'qishni davom ettiring!"
    else:
        emoji = "📚"
        baho = "Hali o'rganish kerak. G'afur G'ulom asarlarini o'qing!"

    stars = "⭐" * (percent // 20)
    return (
        f"{emoji} *Test yakunlandi!*\n\n"
        f"📊 Natija: *{score}/{total}* ({percent}%)\n"
        f"{stars}\n\n"
        f"💬 {baho}"
    )

@router.message(F.text == "🧩 Test")
async def start_quiz(message: Message, state: FSMContext):
    shuffled = random.sample(TESTS, min(10, len(TESTS)))
    await state.set_data({
        "tests": shuffled,
        "current": 0,
        "score": 0,
        "total": len(shuffled)
    })
    await state.set_state(QuizState.playing)

    test = shuffled[0]
    await message.answer(
        f"🧩 *G'AFUR G'ULOM TESTI*\n\n"
        f"Jami: *10 ta* savol\n"
        f"Har bir to'g'ri javob uchun ⭐ ball!\n\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"❓ *1/10 — Savol:*\n\n"
        f"{test['savol']}",
        reply_markup=test_keyboard(test, 0),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("quiz_ans_"))
async def check_answer(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    test_idx = int(parts[2])
    chosen = int(parts[3])

    data = await state.get_data()
    tests = data["tests"]
    score = data["score"]
    current = data["current"]

    if test_idx != current:
        await callback.answer("Bu savol allaqachon o'tilgan!", show_alert=True)
        return

    test = tests[test_idx]
    togri = test["togri"]
    variantlar = test["variantlar"]

    if chosen == togri:
        score += 1
        result_text = (
            f"✅ *To'g'ri!* +1 ball\n\n"
            f"📖 {test['izoh']}"
        )
    else:
        result_text = (
            f"❌ *Noto'g'ri!*\n\n"
            f"To'g'ri javob: *{HARFLAR[togri]}) {variantlar[togri]}*\n\n"
            f"📖 {test['izoh']}"
        )

    next_idx = current + 1
    await state.update_data(score=score, current=next_idx)

    if next_idx >= len(tests):
        # Test tugadi
        await callback.message.edit_text(
            result_text + f"\n\n{'━'*20}\n" + format_result(score, len(tests)),
            reply_markup=result_keyboard(),
            parse_mode="Markdown"
        )
    else:
        next_test = tests[next_idx]
        await callback.message.edit_text(
            result_text +
            f"\n\n{'━'*20}\n"
            f"❓ *{next_idx+1}/{len(tests)} — Savol:*\n\n"
            f"{next_test['savol']}",
            reply_markup=test_keyboard(next_test, next_idx),
            parse_mode="Markdown"
        )

    await callback.answer()

@router.callback_query(F.data.startswith("quiz_skip_"))
async def skip_question(callback: CallbackQuery, state: FSMContext):
    test_idx = int(callback.data.split("_")[2])
    data = await state.get_data()
    tests = data["tests"]
    score = data["score"]
    current = data["current"]

    if test_idx != current:
        await callback.answer("Bu savol allaqachon o'tilgan!", show_alert=True)
        return

    next_idx = current + 1
    await state.update_data(current=next_idx)

    if next_idx >= len(tests):
        await callback.message.edit_text(
            format_result(score, len(tests)),
            reply_markup=result_keyboard(),
            parse_mode="Markdown"
        )
    else:
        next_test = tests[next_idx]
        await callback.message.edit_text(
            f"⏭ *O'tkazib yuborildi*\n\n"
            f"{'━'*20}\n"
            f"❓ *{next_idx+1}/{len(tests)} — Savol:*\n\n"
            f"{next_test['savol']}",
            reply_markup=test_keyboard(next_test, next_idx),
            parse_mode="Markdown"
        )
    await callback.answer()

@router.callback_query(F.data == "quiz_end")
async def end_quiz(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    score = data.get("score", 0)
    total = data.get("total", 10)
    await state.clear()

    await callback.message.edit_text(
        f"🏁 *Test yakunlandi!*\n\n" + format_result(score, total),
        reply_markup=result_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "quiz_restart")
async def restart_quiz(callback: CallbackQuery, state: FSMContext):
    shuffled = random.sample(TESTS, min(10, len(TESTS)))
    await state.set_data({
        "tests": shuffled,
        "current": 0,
        "score": 0,
        "total": len(shuffled)
    })
    await state.set_state(QuizState.playing)

    test = shuffled[0]
    await callback.message.edit_text(
        f"🧩 *G'AFUR G'ULOM TESTI*\n\n"
        f"Yangi test boshlandi!\n\n"
        f"{'━'*20}\n"
        f"❓ *1/10 — Savol:*\n\n"
        f"{test['savol']}",
        reply_markup=test_keyboard(test, 0),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "quiz_home")
async def quiz_home(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Asosiy menyu:", reply_markup=main_menu())
    await callback.answer()
