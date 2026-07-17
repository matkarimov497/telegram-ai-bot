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

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith(("http://", "https://")):
        await update.message.reply_text(
            "YouTube, TikTok, Instagram yoki boshqa video havolasini yuboring."
        )
        return

    status = await update.message.reply_text("⏳ Yuklanmoqda...")

    video_file = None
    audio_file = None

    try:
        # VIDEO
        video_opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "quiet": True,
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
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            base_name = os.path.splitext(
                ydl.prepare_filename(info)
            )[0]
            audio_file = base_name + ".mp3"

        with open(audio_file, "rb") as f:
            await update.message.reply_audio(
                audio=f,
                title=info.get("title", "Audio")
            )

        await status.edit_text("✅ Tayyor!")

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik:\n{e}")

    finally:
        for file_path in [video_file, audio_file]:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download_media
        )
    )

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
