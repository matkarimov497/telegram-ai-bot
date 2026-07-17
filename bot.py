import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8820635879:AAHtAd7Ow2iNk4Zh_xWOCe3yi2VJiL3entI"

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if not url.startswith("http"):
        await update.message.reply_text("Video havolasini yuboring.")
        return

    await update.message.reply_text("Yuklanmoqda...")

    try:
        # Video yuklash
        video_opts = {
            "format": "best",
            "outtmpl": "video.%(ext)s",
        }

        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)

        with open(video_file, "rb") as f:
            await update.message.reply_video(f)

        # Audio yuklash
        audio_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
        }

        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = ydl.prepare_filename(info)

        with open(audio_file, "rb") as f:
            await update.message.reply_audio(f)

        os.remove(video_file)
        os.remove(audio_file)

    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot ishga tushdi...")
app.run_polling()
