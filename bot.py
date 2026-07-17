from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8820635879:AAEu4D8MoANRS-P5jS65p2ZX7WJnMWLgD7o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Havola yuboring."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text.startswith("http://") or text.startswith("https://"):
        context.user_data["url"] = text

        keyboard = [
            [
                InlineKeyboardButton("🎵 MP3", callback_data="mp3"),
                InlineKeyboardButton("🎬 Video", callback_data="video"),
            ]
        ]

        await update.message.reply_text(
            "Formatni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    url = context.user_data.get("url")

    if query.data == "mp3":
        await query.message.reply_text(
            f"MP3 tanlandi.\nURL: {url}"
        )

    elif query.data == "video":
        await query.message.reply_text(
            f"Video tanlandi.\nURL: {url}"
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)
)

app.run_polling()
