import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === AAPKI DETAILS BHAR DI HAIN ===
BOT_TOKEN = "8808135127:AAFrNotIqrR6_qIDJeGRj-3bb6ScvPR9TtE"
ADMIN_ID = 8534490009
CHANNEL_LINK = "https://t.me/+eETcGp4GVUMwNzQ1"

logging.basicConfig(level=logging.INFO)
user_mapping = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Aap Admin hain. Users ke messages yahan aayenge.")
        return
    
    welcome_text = f"❤️ Join Our Channel 👇\n{https://t.me/+eETcGp4GVUMwNzQ1}"
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # User message -> Admin ko milega
    if user_id != ADMIN_ID:
        copied_msg = await update.message.copy(chat_id=ADMIN_ID)
        user_mapping[copied_msg.message_id] = user_id

    # Admin reply -> User ko jayega
    elif user_id == ADMIN_ID and update.message.reply_to_message:
        replied_msg_id = update.message.reply_to_message.message_id
        if replied_msg_id in user_mapping:
            target_user_id = user_mapping[replied_msg_id]
            try:
                await update.message.copy(chat_id=target_user_id)
            except Exception as e:
                await update.message.reply_text(f"❌ Message nahi gaya: {e}")

if name == 'main':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    app.run_polling()
