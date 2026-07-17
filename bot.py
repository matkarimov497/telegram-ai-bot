from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8820635879:AAEu4D8MoANRS-P5jS65p2ZX7WJnMWLgD7o"

MOVIES = {
    "1001": "https://t.me/kinolar1227/2",
    "1002": "https://t.me/kinolar1227/3",
    "1003": "https://t.me/kinolar1227/4",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎬 Kino botga xush kelibsiz!\n\n"
        "Kino kodini yuboring."
    )
    await update.message.reply_text(text)

async def find_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()

    if code in MOVIES:
        await update.message.reply_text(
            f"🎥 Kino havolasi:\n{MOVIES[code]}"
        )
    else:
        await update.message.reply_text(
            "❌ Bunday kino topilmadi."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, find_movie)
)

app.run_polling()
