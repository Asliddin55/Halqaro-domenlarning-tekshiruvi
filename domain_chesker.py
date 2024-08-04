import aiohttp
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode

# Tokenni bevosita kodga kiritamiz
bot_token = 'Bot_Tokeningzni_kiriting'

# Loggerni sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Botni yaratish
bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Domenni tekshirish uchun yordamchi funksiya
async def check_domain_status(domain: str) -> str:
    url = f"https://{domain}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return "Domen mavjud va ishlamoqda."
                else:
                    return "Domen mavjud, lekin server javob bermadi."
    except aiohttp.ClientError:
        return "Domen bant qilingan yoki mavjud emas."

# /check domen komandasiga handler
@dp.message_handler(commands=['check'])
async def check_domain(message: types.Message):
    domain = message.get_args()
    if not domain:
        await message.reply("Iltimos, tekshiriladigan domenni kiriting. Misol: /check example.com")
        return

    status = await check_domain_status(domain)
    await message.reply(f"Domen {domain} holati: {status}")

# Botni ishga tushirganda /start komandasi yuborilishi uchun funksiya
async def on_startup(dp):
    # Bot ishga tushganida /start komandasi yuboriladi
    admins = [6188085308]  # Adminlar ro'yxati
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, "Bot ishga tushdi!")
            await bot.send_message(admin_id, "/check komandasi yordamida domen holatini tekshirishingiz mumkin.")
        except Exception as e:
            logger.error(f"Xato yuz berdi: {e}")

# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
