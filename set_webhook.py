import os
import asyncio
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = os.environ["BASE_URL"]

async def set_webhook():
    bot = Bot(token=TOKEN)
    await bot.set_webhook(f"{BASE_URL}/webhook/{TOKEN}")
    print("✅ Webhook Set!")

if __name__ == "__main__":
    asyncio.run(set_webhook())
