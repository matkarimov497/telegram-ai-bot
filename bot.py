from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8820635879:AAEu4D8MoANRS-P5jS65p2ZX7WJnMWLgD7o"

MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["🎵 MP3 Yuklash"],
        ["ℹ️ Yordam", "📢 Kanal"],
        ["👤 Profil"],
    ],
    resize_keyboard=True,
)

CHANNEL_LINK = "https://t.me/kinolar1227"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎵 MP3 Downloader Bot\n\n"
        "Xush kelibsiz!\n\n"
        "Video havolasini yuboring.\n"
        "Pastdagi menyudan foydalaning 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=MAIN_MENU,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "🎵 MP3 Yuklash":
        await update.message.reply_text(
            "🔗 Video havolasini yuboring."
        )
        return

    if text == "ℹ️ Yordam":
        await update.message.reply_text(
            "1. Havolani yuboring\n"
            "2. Bot uni tekshiradi\n"
            "3. Natijani qaytaradi"
        )
        return

    if text == "📢 Kanal":
        await update.message.reply_text(CHANNEL_LINK)
        return

    if text == "👤 Profil":
        user = update.effective_user

        await update.message.reply_text(
            f"👤 Profil\n\n"
            f"ID: {user.id}\n"
            f"Ism: {user.first_name}"
        )
        return

    if text.startswith("http://") or text.startswith("https://"):
        await update.message.reply_text(
            "✅ Havola qabul qilindi."
        )
        return

    await update.message.reply_text(
        "❌ Noma'lum buyruq."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

app.run_polling()
