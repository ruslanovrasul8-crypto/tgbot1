from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8972777482:AAGoKL0E5Hbi6HeWoGIxFwhsRyT3FcnzntM"

ADMINS = [8504521646, 8892000845]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ожидайте ответа администратора")

    username = update.effective_user.username or "no_username"

    for admin in ADMINS:
        await context.bot.send_message(
            chat_id=admin,
            text=f"📩 Новый пользователь: @{username}"
        )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    username = user.username or "no_username"

    # если админ отвечает
    if user.id in ADMINS:
        if update.message.reply_to_message:
            try:
                target = update.message.reply_to_message.text
                target = target.split("@")[1].split("\n")[0]

                await context.bot.send_message(
                    chat_id=target,
                    text=text
                )
            except:
                await update.message.reply_text("Ошибка ответа")
        return

    # пользователь → админы
    for admin in ADMINS:
        await context.bot.send_message(
            chat_id=admin,
            text=f"👤 @{username}\n💬 {text}"
        )

    await update.message.reply_text("Отправлено")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()