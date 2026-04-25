from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🧩 Test"),
                KeyboardButton(text="📚 Kitoblar")
            ],
            [
                KeyboardButton(text="🎧 Audio hikoyalar"),
                KeyboardButton(text="📖 Asarlari haqida")
            ],
            [
                KeyboardButton(text="ℹ️ Tarjimayi hol"),
                KeyboardButton(text="🎭 She'rlar")
            ],
            [
                KeyboardButton(text="❓ Yordam")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Menyu tanlang..."
    )

def books_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📗 Shum bola", callback_data="book_shum_bola")],
            [InlineKeyboardButton(text="📘 Mening o'g'rigina bolam", callback_data="book_ogrigina")],
            [InlineKeyboardButton(text="📙 Ko'cha bolasi", callback_data="book_kucha")],
            [InlineKeyboardButton(text="📕 Sariq devlar", callback_data="book_sariq_devlar")],
            [InlineKeyboardButton(text="📓 Navoiy", callback_data="book_navoiy")],
            [InlineKeyboardButton(text="📒 To'la asarlar to'plami", callback_data="book_tola")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
        ]
    )

def audio_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎙️ Shum bola (audio)", callback_data="audio_shum_bola")],
            [InlineKeyboardButton(text="🎙️ She'rlar o'qilishi", callback_data="audio_sherlar")],
            [InlineKeyboardButton(text="🎙️ Hikoyalar", callback_data="audio_hikoyalar")],
            [InlineKeyboardButton(text="🎙️ Asarlari (to'liq)", callback_data="audio_full")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
        ]
    )

def works_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ She'rlar", callback_data="works_poems")],
            [InlineKeyboardButton(text="📝 Hikoyalar", callback_data="works_stories")],
            [InlineKeyboardButton(text="🎭 Qissalar", callback_data="works_novels")],
            [InlineKeyboardButton(text="🎬 Tarjimalar", callback_data="works_drama")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
        ]
    )

def cancel_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_chat")]
        ]
    )
