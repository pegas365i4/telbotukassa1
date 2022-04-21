from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# --- Main Menu ---
btnSub = KeyboardButton('❤ ПОДПИСКА')
btnSettings = KeyboardButton('🛠 НАСТРОЙКИ')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnSub)
mainMenu.add(btnSettings)

# --- Subscribe Inline Buttons ---
sub_inline_markup = InlineKeyboardMarkup(row_width=1)

btnSubMonth = InlineKeyboardButton(text="Месяц - 150 рублей", callback_data="submonth")

sub_inline_markup.insert(btnSubMonth)
