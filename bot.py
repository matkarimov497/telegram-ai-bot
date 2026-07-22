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

import os

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Video yoki audio link yuboring."
    )


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith(("http://", "https://")):
        await update.message.reply_text(
            "Iltimos video yoki audio havolasini yuboring."
        )
        return

    try:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": "%(title)s.%(ext)s",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if not os.path.exists(filename):
                base = os.path.splitext(filename)[0]
                if os.path.exists(base + ".mp4"):
                    filename = base + ".mp4"

        with open(filename, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=os.path.basename(filename)
            )

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
