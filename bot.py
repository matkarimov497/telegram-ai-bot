import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8820635879:AAFpAj-eSAJopBvakUstblyJVyD7T0dn_G8"

os.makedirs("downloads", exist_ok=True)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("Link yuboring.")
        return

    await update.message.reply_text("⏳ Yuklanmoqda...")

    video_file = None
    audio_file = None

    try:
        # Video
        video_opts = {
            "format": "best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)

        with open(video_file, "rb") as f:
            await update.message.reply_video(
                video=f,
                caption="🎬 Video"
            )

        # MP3
        audio_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }

        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = os.path.splitext(
                ydl.prepare_filename(info)
            )[0] + ".mp3"

        with open(audio_file, "rb") as f:
            await update.message.reply_audio(
                audio=f,
                title=info.get("title", "MP3")
            )

        # Tozalash
        if video_file and os.path.exists(video_file):
            os.remove(video_file)

        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik:\n{e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        download
    )
)

print("Bot ishga tushdi...")
app.run_polling()
