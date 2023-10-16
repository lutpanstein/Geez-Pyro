from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent
from Geez import app

# Dictionary untuk menyimpan username/id target
whisper_targets = {}

# Fungsi untuk menangani perintah /start
@app.on_message(filters.command("start"))
def start(_, message):
    message.reply_text("Halo! Saya bot rahasia. Kirimkan pesan rahasia dengan mengetik /whisper.")

# Fungsi untuk menangani perintah /whisper
@app.on_message(filters.command("whisper"))
def whisper(_, message):
    if message.chat.type == "private":
        message.reply_text("Kirimkan pesan rahasia ini kepada pengguna lain:")
        whisper_targets[message.chat.id] = True

# Fungsi untuk menangani inline query
@app.on_inline_query()
def inline_query(_, query):
    if query.query.startswith("whisper"):
        results = []
        username = query.query.split(" ", 1)[-1]
        whisper_targets[query.from_user.id] = username
        button = [
            [InlineKeyboardButton("Buka Pesan", switch_inline_query_current_chat=f"whisper {username}")]
        ]
        markup = InlineKeyboardMarkup(button)
        input_message_content = InputTextMessageContent(f"Pesan rahasia untuk {username}")
        results.append(
            {
                "type": "article",
                "id": "1",
                "title": "Kirim Pesan Rahasia",
                "input_message_content": input_message_content,
                "reply_markup": markup
            }
        )
        query.answer(results)

# Fungsi untuk menangani pesan rahasia
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
