import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

TOKEN = "8808135127:AAFrNotIqrR6_qIDJeGRj-3bb6ScvPR9TtE"
ADMIN_ID = 8534490009
CHANNEL_LINK = "https://t.me/+eETcGp4GVUMwNzQ1"

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Join Channel", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Click below to join:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id == ADMIN_ID:
        if update.message.reply_to_message:
            try:
                orig_text = update.message.reply_to_message.text or ""
                target_id = int(orig_text.split("ID: ")[1].split(")")[0])
                await context.bot.send_message(chat_id=target_id, text=update.message.text)
                await update.message.reply_text("Message sent to user.")
            except Exception as e:
                await update.message.reply_text("Could not send reply. Make sure you replied to a forwarded message containing the user ID.")
    else:
        forward_text = f"From: {user.first_name} (ID: {user.id})\n\n{update.message.text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)
        await update.message.reply_text("Your message has been sent to the admin.")

if __name__ == '__main__':
    threading.Thread(target=run_health_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
                                      
