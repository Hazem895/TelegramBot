import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive  # لتشغيل السيرفر الوهمي

keep_alive()

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ["BOT_TOKEN"]
GROUP_CHAT_ID = os.environ["GROUP_CHAT_ID"]
ALLOWED_USERS = ALLOWED_USERS = list(map(int, os.environ["ALLOWED_USERS"].split(",")))
users_set = set()

# أمر /start في الخاص
# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/start used by {user.id} - {user.full_name}")
    await update.message.reply_text("👋 أهلاً! البوت شغال على Webhook.")

async def start_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/startclass used by {user.id} - {user.full_name}")
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
    
# /chatid
async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: {chat.id}")

# إعداد التطبيق وتشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("startclass", start_class))
app.add_handler(CommandHandler("myid", my_id))
app.add_handler(CommandHandler("chatid", chat_id))
app.add_handler(CommandHandler("mentionall", mention_all))

app.run_polling()