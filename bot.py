import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive  # لتشغيل السيرفر الوهمي

keep_alive()

TOKEN = os.environ["BOT_TOKEN"]
GROUP_CHAT_ID = os.environ["GROUP_CHAT_ID"]
ALLOWED_USERS = os.environ["ALLOWED_USERS"]

# أمر /start في الخاص
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! هبلغكوا لما الحصة تبدأ.")

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

# إعداد التطبيق وتشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("start_class", start_class))
app.add_handler(CommandHandler("myid", my_id))
app.add_handler(CommandHandler("chatid", chat_id))

app.run_polling()
