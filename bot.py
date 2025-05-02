# bot.py - Main bot entry point
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from meme_engine import generate_meme
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🖼️ *Welcome to MemesterBot!*\n"
        "Send /memes to choose a template or upload an image with text!\n"
        "Example: Send a photo with caption *'Top Text|Bottom Text'*",
        parse_mode="Markdown"
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📌 *Commands:*\n"
        "/start - Welcome message\n"
        "/help - Show this menu\n"
        "/memes - Browse meme templates\n"
        "/fonts - List available fonts\n"
        "/credits - Bot info",
        parse_mode="Markdown"
    )

def list_memes(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Distracted BF", callback_data="template_distracted_bf")],
        [InlineKeyboardButton("Drake Hotline", callback_data="template_drake")],
        [InlineKeyboardButton("Two Buttons", callback_data="template_buttons")]
    ]
    update.message.reply_text(
        "🎭 Choose a template:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def template_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    # Store selected template in user context
    context.user_data["selected_template"] = query.data
    query.edit_message_text(text=f"Selected: {query.data.replace('template_', '').replace('_', ' ')}\nNow send your text as 'Top|Bottom'")

def handle_photo(update: Update, context: CallbackContext):
    photo = update.message.photo[-1].get_file()
    caption = update.message.caption

    if caption and "|" in caption:
        top_text, bottom_text = caption.split("|", 1)
        meme_bytes = generate_meme(photo.download_as_bytearray(), top_text.strip(), bottom_text.strip())
        update.message.reply_photo(photo=meme_bytes)
    else:
        context.user_data["pending_photo"] = photo
        update.message.reply_text("🔤 Now send the text format: *'Top|Bottom'*", parse_mode="Markdown")

def handle_text(update: Update, context: CallbackContext):
    if "pending_photo" in context.user_data:
        text = update.message.text
        if "|" in text:
            top_text, bottom_text = text.split("|", 1)
            photo = context.user_data["pending_photo"]
            meme_bytes = generate_meme(photo.download_as_bytearray(), top_text.strip(), bottom_text.strip())
            update.message.reply_photo(photo=meme_bytes)
            del context.user_data["pending_photo"]

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("memes", list_memes))

    # Message handlers
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Callback handlers
    dp.add_handler(CallbackQueryHandler(template_selected, pattern="^template_"))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
