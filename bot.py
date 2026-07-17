import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8820635879:AAEu4D8MoANRS-P5jS65p2ZX7WJnMWLgD7o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Link yuboring.\n\n"
        "Video uchun: link yuboring\n"
        "Audio uchun: /mp3 link"
    )

async def video_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    try:
        await update.message.reply_text("📥 Video yuklanmoqda...")

        ydl_opts = {
            "format": "best",
            "outtmpl": "%(title)s.%(ext)s"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as f:
            await update.message.reply_video(f)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")

async def mp3_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Misol:\n/mp3 https://...")
        return

    url = context.args[0]

    try:
        await update.message.reply_text("🎵 Audio yuklanmoqda...")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as f:
            await update.message.reply_audio(
                audio=f,
                title=info.get("title", "Audio")
            )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mp3", mp3_download))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, video_download)
)

app.run_polling()
