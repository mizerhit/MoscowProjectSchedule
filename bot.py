from aiogram import Bot, executor, Dispatcher, types


token = '6811512405:AAGrLqg52kIxSfkSFg9DzYyvJEPKqq4sprc'
bot = Bot(token=token)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['help', 'start'])
async def cmd_start(msg: types.Message) -> None:
    await msg.answer('Hello! I can tell your schedule')

@dp.message_handler()
async def send_echo(msg: types.Message) -> None:
    await msg.answer(msg.text)
    await bot.send_message(chat_id=msg.from_user.id, text=f'{msg.text} _ {msg.from_user.full_name}')

if __name__ == '__main__':
    executor.start_polling(dp)