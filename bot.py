from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8820635879:AAGlvYwFHMAI_NiHNyNOziupHx0JpA55urY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Video yoki audio link yuboring."
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_document(open(filename, "rb"))

    except Exception as e:
        await update.message.reply_text(f"Xato: {e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

app.run_polling()
