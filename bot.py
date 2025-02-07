from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Your bot token and admin ID
BOT_TOKEN = "7842830406:AAHn5vmaOqofHQT7KEn3vZwC2HgEzIU_Pj0"
ADMIN_ID = 7298143104  # Your Telegram numeric ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# User keyboard with "Ask Admin" button
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Ask Admin"))

# Start command
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Welcome! Click 'Ask Admin' to send a message to the admin.", reply_markup=keyboard)

# "Ask Admin" button response
@dp.message_handler(lambda message: message.text == "Ask Admin")
async def ask_admin(message: types.Message):
    await message.reply("Please type your message below. I will forward it to the admin.")

# Forward user messages to the admin
@dp.message_handler()
async def forward_to_admin(message: types.Message):
    user_info = f"📩 Message from @{message.from_user.username or 'No Username'} (ID: {message.from_user.id}):\n"
    reply_tag = f"Reply{message.from_user.id}"  # Unique identifier for replies
    await bot.send_message(ADMIN_ID, f"{user_info}{message.text}\n\n🔁 Reply using: {reply_tag} [your message]")
    await message.reply("✅ Your message has been sent to the admin.")

# Admin replies to users
@dp.message_handler(lambda message: message.chat.id == ADMIN_ID and message.text.startswith("Reply"))
async def admin_reply(message: types.Message):
    try:
        parts = message.text.split(" ", 1)  # Split into reply tag and actual message
        user_id = int(parts[0].replace("Reply", ""))  # Extract user ID
        reply_text = parts[1]  # Extract the actual reply

        await bot.send_message(user_id, f"📩 Admin's Reply:\n{reply_text}")
        await message.reply("✅ Your reply has been sent.")
    except (IndexError, ValueError):
        await message.reply("❌ Incorrect reply format. Use: Reply<USER_ID> [your message]")

# Start the bot
executor.start_polling(dp)
