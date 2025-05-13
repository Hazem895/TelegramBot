from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
TOKEN = os.environ["BOT_TOKEN"]
GROUP_CHAT_ID = os.environ["GROUP_CHAT_ID"]
ADMIN_USER_IDS= os.environ["ADMIN_USER_IDS"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هبلغكوا لما الحصة تبدأ 📢")

async def notify_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # بس الإدمن يقدر يبعت الأمر ده
    user = update.effective_user
    if user and user.id in ADMIN_USER_IDS:  # حط ID بتاعك هنا
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text="📚 الحصة بدأت! يلا كلكم ركزوا!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("start_class", notify_class))  # الأمر اللي هيبعت الرسالة للجروب

app.run_polling()
