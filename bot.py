import os
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# إعدادات البيئة
TOKEN = os.environ["BOT_TOKEN"]
GROUP_CHAT_ID = int(os.environ["GROUP_CHAT_ID"])
ALLOWED_USERS = list(map(int, os.environ["ALLOWED_USERS"].split(",")))
users_set = set()

# Logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI App
app = FastAPI()
bot_app = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! البوت شغال على Webhook.")

async def start_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in ALLOWED_USERS:
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text="📚 الحصة بدأت! يلا نبدأ!")
    else:
        await update.message.reply_text("❌ مش مسموحلك تستخدم الأمر ده.")

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🪪 ID بتاعك هو: {update.effective_user.id}")

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
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("startclass", start_class))
bot_app.add_handler(CommandHandler("myid", my_id))
bot_app.add_handler(CommandHandler("chatid", chat_id))
bot_app.add_handler(CommandHandler("mentionall", mention_all))
bot_app.add_handler(MessageHandler(filters.TEXT & filters.Chat(GROUP_CHAT_ID), register_user))

# FastAPI webhook endpoint
@app.post(f"/webhook/{TOKEN}")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Bot is running with Webhook!"}
