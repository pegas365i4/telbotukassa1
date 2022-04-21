import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import markups as nav # Сократил название, чтобы было удобнее


TOKEN = "5******3:A***************************4" # input my token
YOOTOKEN = "3******8:TEST:3****8" # input token Юкассы [Если выбран бот ЮKassa: тест]
# Как получить своего бота к боту ЮKassa
# (https://yookassa.ru/docs/support/payments/onboarding/integration/cms-module/telegram)

logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Приветственное сообщение и включает отображение главого меню с кнопками:
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добрый день', reply_markup=nav.mainMenu)

# Ловит все сообщения и ищет '❤ ПОДПИСКА'. Потом выдает новое сообщение с товаром и кнопкой инлайн:
@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private': # РАБОТАЕТ ТОЛЬКО В ПРИВАТНОМ РЕЖИМЕ!
        if message.text == '❤ ПОДПИСКА':
            await bot.send_message(message.from_user.id, 'Описание возможностей подписки', reply_markup=nav.sub_inline_markup)

# Создаём декоратор
@dp.callback_query_handler(text="submonth")
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id) # Удалил предыдущее сообщение
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки", description="Тестовое описание товара", payload="month_sub", provider_token=YOOTOKEN, currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 15000}])

# Подтверждаем, что у нас есть нужный товар в наличии:
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Подхватываем, что наш товар уже оплачен и выдаем сообщение об удачной покупке:
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        # Подписываем пользователя
        await bot.send_message(message.from_user.id, "Вам выдана подписка на месяц!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)