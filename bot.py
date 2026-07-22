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

TOKEN = os.getenv("TOKEN")

# Foydalanuvchi yuborgan oxirgi link
user_urls = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Video yoki audio havolasini yuboring."
    )


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # MP3 tugmasi bosilganda
    if text == "🎵 MP3 Yuklash":
        url = user_urls.get(update.effective_user.id)

        if not url:
            await update.message.reply_text(
                "Avval video havolasini yuboring."
            )
            return

        try:
            await update.message.reply_text("MP3 tayyorlanmoqda...")

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "%(title)s.%(ext)s",
                "noplaylist": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            filename = f"{info['title']}.mp3"

            with open(filename, "rb") as audio:
                await update.message.reply_audio(
                    audio=audio,
                    title=info.get("title", "Audio")
                )

            if os.path.exists(filename):
                os.remove(filename)

        except Exception as e:
            await update.message.reply_text(f"Xato: {e}")

        return

    # URL tekshirish
    if not text.startswith(("http://", "https://")):
        await update.message.reply_text(
            "Iltimos video yoki audio havolasini yuboring."
        )
        return

    # URL saqlash
    user_urls[update.effective_user.id] = text

    try:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": "%(title)s.%(ext)s",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            filename = ydl.prepare_filename(info)

        if not os.path.exists(filename):
            base = os.path.splitext(filename)[0]
            if os.path.exists(base + ".mp4"):
                filename = base + ".mp4"

        with open(filename, "rb") as video:
            await update.message.reply_document(
                document=video,
                filename=os.path.basename(filename)
            )

        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"Xato: {e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download
        )
    )

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
