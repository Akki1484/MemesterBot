from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
     from meme_engine import generate_meme
     import os

     TOKEN = os.getenv("7554530234:AAFaSDdysUnh35_NqzQ4XKBF3iKvH3O_AO8")

     def start(update, context):
         update.message.reply_text("🎨 Send /memes or upload an image to make a meme!")

     # Add other handlers (image processing, commands)
     updater = Updater(TOKEN)
     updater.dispatcher.add_handler(CommandHandler("start", start))
     updater.start_polling()
