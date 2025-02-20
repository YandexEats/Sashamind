from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7612365999:AAEUZ8h4pXmMQoo-xbypdzcYZLoVqbGHe2s"  # ЗАМЕНИ НА СВОЙ ТОКЕН
OWNER_ID = 1777308158  # ЗАМЕНИ НА СВОЙ TELEGRAM ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == OWNER_ID:
        await update.message.reply_text("Привет, хозяин!")
    else:
        await update.message.reply_text("Тебе тут че делать? 🤨")

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        warned_user = update.message.reply_to_message.from_user
        await update.message.reply_text(f"{warned_user.first_name} получил предупреждение!")
    else:
        await update.message.reply_text("Ответьте на сообщение участника, чтобы дать предупреждение!")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        banned_user = update.message.reply_to_message.from_user
        chat_id = update.effective_chat.id
        await context.bot.ban_chat_member(chat_id, banned_user.id)
        await update.message.reply_text(f"{banned_user.first_name} был забанен!")
    else:
        await update.message.reply_text("Ответьте на сообщение участника, чтобы забанить!")

async def delete_join_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        try:
            await update.message.delete()
        except Exception as e:
            print(f"Ошибка при удалении сообщения о входе: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex("!пред"), warn))
app.add_handler(MessageHandler(filters.Regex("!бан"), ban))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, delete_join_message))
app.add_error_handler(error_handler)

print("Бот запущен!")
app.run_polling()