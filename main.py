import logging
from aiogram import Bot, Dispatcher, executor, types

from oxfordLookup import getDefinitions
from googletrans import Translator
translator = Translator()

API_TOKEN = "5882639467:AAGz5viLDYKr3JSJC7fR4B8RjVgZVQMTEuM"


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Salom!\n"
                         "/start: Boshlash.\n"
                         "/help: Yordamdan foydalanish.\n"
                         "/info: Bot haqida ma'lumot.\n")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer("🤷🏻‍Bizda o'ziga o'zi hizmat, biz sizga hech qanday yordam bera olmaymiz. UZR!!")


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Bu botda siz so'zlarni audio holida olishingiz,\n"
        "Biror narsa haqida ingliz tilida ma'lumotlar olishingiz mumkin.")


@dp.message_handler()
async def tarjimon(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        # translator.translate('안녕하세요.', dest='ja')
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
