from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

def start(update, context):
    update.message.reply_text("Hello there!")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
