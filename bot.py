import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables (for security)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your bot token
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Your Telegram User ID

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

# Dictionary to store user IDs for replies
user_data = {}

# Function to handle /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Send me a message, and I'll forward it to the admin.")

# Function to handle user messages and forward them to admin
def forward_to_admin(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_message = update.message.text
    user_data[user.id] = user  # Store user details for replies
    
    # Forward message to admin
    bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 New message from {user.first_name} (@{user.username} | ID: {user.id}):\n{user_message}"
    )
    
    # Notify the user
    update.message.reply_text("✅ Your message has been sent to the admin.")

# Function to handle admin replies
def reply_to_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        admin_reply = update.message.text
        original_message = update.message.reply_to_message.text
        
        # Extract user ID from original message
        if "ID:" in original_message:
            user_id_start = original_message.rfind("ID:") + 4
            user_id = int(original_message[user_id_start:].strip())
            
            # Send reply to the user
            bot.send_message(chat_id=user_id, text=f"📢 Admin's reply: {admin_reply}")
            update.message.reply_text("✅ Reply sent successfully.")

# Main function to run the bot
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))

    # Message handlers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_to_admin))
    dp.add_handler(MessageHandler(Filters.reply & Filters.text, reply_to_user))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

