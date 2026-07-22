import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
import yt_dlp

TOKEN = "8820635879:AAGVWgxQnb6OkyIDKqkCbiwVMgplzFN5if0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def download_video(message: types.Message):
    url = message.text

    if not url.startswith("http"):
        await message.answer("Video link yuboring.")
        return

    await message.answer("📥 Video yuklanmoqda...")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }

    os.makedirs("downloads", exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        files = [f for f in os.listdir("downloads") if f.endswith(".mp4")]

        if files:
            video = os.path.join("downloads", files[0])

            await message.answer_video(
                FSInputFile(video),
                caption="✅ Eng yuqori sifatda yuklandi"
            )

            os.remove(video)

        else:
            await message.answer("❌ Video topilmadi.")

    except Exception as e:
        await message.answer(f"Xatolik: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
