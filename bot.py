import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# إعداد اللوجز
logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# تحميل المتغيرات
load_dotenv()
TOKEN = os.environ["BOT_TOKEN"]
GROUP_CHAT_ID = int(os.environ["GROUP_CHAT_ID"])
ALLOWED_USERS = list(map(int, os.environ["ALLOWED_USERS"].split(",")))

bot = Bot(token=TOKEN)
app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

users_set = set()

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/start used by {user.id} - {user.full_name}")
    await update.message.reply_text("👋 أهلاً! البوت شغال على Webhook.")

async def start_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in ALLOWED_USERS:
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text="📚 الحصة بدأت! يلا نبدأ!")
    else:
        await update.message.reply_text("❌ مش مسموحلك تستخدم الأمر ده.")

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/myid used by {user.id} - {user.full_name}")
    await update.message.reply_text(f"🪪 ID بتاعك هو: {user.id}")

async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        users_set.add(user.id)
        logger.info(f"User registered: {user.id} - {user.full_name}")

async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: {chat.id}")

async def mention_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in ALLOWED_USERS:
        await update.message.reply_text("❌ مش مسموحلك تستخدم الأمر ده.")
        return
    if not users_set:
        await update.message.reply_text("⚠️ مفيش أعضاء مسجلين لسه.")
        return
    mentions = [f"[شخص](tg://user?id={uid})" for uid in users_set]
    text = "📢 منشن لكل المسجلين:\n" + " ".join(mentions)
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=text, parse_mode=ParseMode.MARKDOWN)

# Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("start_class", start_class))
application.add_handler(CommandHandler("myid", my_id))
application.add_handler(CommandHandler("chatid", chat_id))
application.add_handler(CommandHandler("mention_all", mention_all))
application.add_handler(MessageHandler(filters.TEXT & filters.Chat(GROUP_CHAT_ID), register_user))

# Routes
@app.route("/")
def home():
    return "بوت شغال ✅"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "ok"

# Webhook run
if __name__ == "__main__":
    try:
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{os.environ['RENDER_URL']}/{TOKEN}"
    )
except Exception as e:
    logger.error(f"Error occurred: {e}")
    )
