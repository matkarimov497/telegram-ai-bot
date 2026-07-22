import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8820635879:AAGQGuPqyCbwal8VXeHQcx8J7K3oCdzqm-0")
URL_REGEX = r"https?://[^\s]+"

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    urls = re.findall(URL_REGEX, text)
    if not urls:
        return

    url = urls[0]

    await update.message.reply_text("⏳ Yuklanmoqda...")

    try:
        ydl_opts = {
            "format": "best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "noplaylist": True,
        }

        os.makedirs("downloads", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        size = os.path.getsize(filename)

        if size < 50 * 1024 * 1024:
            with open(filename, "rb") as f:
                await update.message.reply_video(f)
        else:
            with open(filename, "rb") as f:
                await update.message.reply_document(f)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download)
    )

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
