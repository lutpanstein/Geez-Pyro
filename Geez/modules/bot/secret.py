from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from Geez import app

# Fungsi untuk menangani perintah /start
@app.on_message(filters.command(["start"]))
def start_command(client, message):
    # Mengirim pesan awal
    client.send_message(
        chat_id=message.chat.id,
        text="Halo! Silakan gunakan perintah /secret untuk membuat pesan rahasia."
    )

# Fungsi untuk menangani perintah /secret
@app.on_message(filters.command(["secret"]))
def secret_command(client, message):
    # Memeriksa apakah pesan memiliki argumen yang valid
    if len(message.command) < 3:
        client.send_message(
            chat_id=message.chat.id,
            text="Format perintah salah. Gunakan /secret <pesan tujuan> <username/id>."
        )
        return

    # Mendapatkan pesan tujuan dan username/id pengguna
    target_message = message.command[1]
    target_user = message.command[2]

    # Membuat inline keyboard dengan tombol untuk membuka pesan rahasia
    inline_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Buka Pesan Rahasia", switch_inline_query=f"{target_message} {target_user}")]]
    )

    # Mengirim pesan dengan inline keyboard
    client.send_message(
        chat_id=message.chat.id,
        text="Pesan rahasia telah dibuat!",
        reply_markup=inline_keyboard
    )

# Fungsi untuk menangani inline query
@app.on_inline_query()
def inline_query(client, query: InlineQuery):
    try:
        # Mendapatkan pesan tujuan dan username/id pengguna dari inline query
        target_message, target_user = query.query.split()

        # Membuat pesan inline result
        result = [
            InlineQueryResultArticle(
                id="1",
                title="Pesan Rahasia",
                input_message_content=InputTextMessageContent(f"Ini adalah pesan rahasia untuk @{target_user}: {target_message}")
            )
        ]

        # Mengirim hasil inline query
        client.answer_inline_query(query.id, results=result)

    except ValueError:
        pass
