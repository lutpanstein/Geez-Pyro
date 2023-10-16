from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent
from Geez import app

whisper_targets = {}

@app.on_message(filters.command("start"))
def start(_, message):
    message.reply_text("Halo! Saya bot rahasia. Kirimkan pesan rahasia dengan mengetik /whisper.")

@app.on_message(filters.command("whisper"))
def whisper(_, message):
    if message.chat.type == "private":
        message.reply_text("Kirimkan pesan rahasia ini kepada pengguna lain:")
        whisper_targets[message.from_user.id] = True

@app.on_inline_query()
def inline_query(_, query):
    if query.query.startswith("whisper"):
        username = query.query.split(" ", 1)[-1]
        whisper_targets[query.from_user.id] = username
        button = [
            [InlineKeyboardButton("Buka Pesan", switch_inline_query_current_chat=f"whisper {username}")]
        ]
        markup = InlineKeyboardMarkup(button)
        input_message_content = InputTextMessageContent(f"Pesan rahasia untuk {username}")
        results = [
            {
                "type": "article",
                "id": "1",
                "title": "Kirim Pesan Rahasia",
                "input_message_content": input_message_content,
                "reply_markup": markup
            }
        ]
        query.answer(results)

@app.on_chosen_inline_result()
def chosen_inline_result(_, result):
    if result.query.startswith("whisper"):
        username = result.query.split(" ", 1)[-1]
        user_id = whisper_targets.get(result.from_user.id)
        if user_id and username == user_id:
            result_message = f"Pesan rahasia untuk {username}"
            app.send_message(result.from_user.id, result_message)
        else:
            app.send_message(result.from_user.id, "Anda tidak memiliki izin untuk melihat pesan ini.")

@app.on_message(filters.private & ~filters.me & filters.text)
def mention(_, message):
    user = message.from_user
    if f"@{app.get_me().username}" in message.text:
        message.reply_text(f"Halo, {user.first_name}!\n\nUntuk mengirim pesan rahasia, ketik /whisper.")


