import os
import yt_dlp

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8820635879:AAHtAd7Ow2iNk4Zh_xWOCe3yi2VJiL3entI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 Link yuboring\n\n"
        "🎥 Video: link yuboring\n"
        "🎵 MP3: /mp3 link",
        reply_markup=ReplyKeyboardRemove()
    )

async def video_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith(("http://", "https://")):
        await update.message.reply_text(
            "❌ Link yuboring.\n\nMisol:\nhttps://youtube.com/..."
        )
        return

    try:
        await update.message.reply_text("📥 Video yuklanmoqda...")

        ydl_opts = {
            "format": "best",
            "outtmpl": "%(title)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as video:
            await update.message.reply_video(video)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")

async def mp3_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🎵 Misol:\n/mp3 https://youtube.com/..."
        )
        return

    url = context.args[0]

    try:
        await update.message.reply_text("🎵 MP3 yuklanmoqda...")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
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

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mp3", mp3_download))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, video_download)
)

print("Bot ishga tushdi...")
app.run_polling()
