import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["BOT_TOKEN"]
bot = Bot(token=TOKEN)
app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()
GROUP_CHAT_ID = os.environ["GROUP_CHAT_ID"]
ALLOWED_USERS = os.environ["ALLOWED_USERS"]
users_set = set()

# أمر /start في الخاص
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! البوت شغال على Webhook.")
    
# أمر /start_class من الأشخاص المصرح لهم
async def start_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user and user.id in ALLOWED_USERS:
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text="📚 الحصة بدأت! يلا نبدأ!")
    else:
        await update.message.reply_text("❌ مش مسموحلك تستخدم الأمر ده.")

# أمر /myid (يساعدك تجيب IDك الشخصي)
async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"🔎 ID بتاعك هو: {user.id}")

# /chatid
async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: {chat.id}")

async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        users_set.add(user.id)

async def mention_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user and user.id not in ALLOWED_USERS:
        await update.message.reply_text("❌ مش مسموحلك تستخدم الأمر ده.")
        return

    if not users_set:
        await update.message.reply_text("⚠️ مفيش أعضاء مسجلين لسه.")
        return

    mentions = []
    for user_id in users_set:
        mentions.append(f"[شخص](tg://user?id={user_id})")
    text = "📢 منشن لكل المسجلين:" + " ".join(mentions)
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=text, parse_mode=ParseMode.MARKDOWN)

# إعداد التطبيق وتشغيل البوت
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("start_class", start_class))
application.add_handler(CommandHandler("myid", my_id))
application.add_handler(CommandHandler("chatid", chat_id))
application.add_handler(CommandHandler("mention_all", mention_all))
application.add_handler(MessageHandler(filters.TEXT & filters.Chat(GROUP_CHAT_ID), register_user))  # تسجيل كل اللي بيبعتوا

@app.route("/")
def index():
    return "بوت شغال ✅"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    return application.update(update)

if __name__ == "__main__":
    # شغّل webhook لما ترفع على سيرفر
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{os.environ['RENDER_URL']}/{TOKEN}"
    )