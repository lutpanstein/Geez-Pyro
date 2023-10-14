from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Geez import app


# Fungsi untuk mengirim pesan rahasia
@app.on_message(filters.command(["start"]))
def start(client, message):
    message.reply_text(
        "Halo! Untuk mengirim pesan rahasia, gunakan format:\n\n"
        "@usernamebot <pesan> <@username_target>\n\n"
        "Gunakan tombol di bawah untuk membuka pesan rahasia.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Buka Pesan Rahasia", callback_data='unlock')]])
    )

# Fungsi untuk membuka pesan rahasia
@app.on_callback_query(filters.regex('^unlock$'))
def unlock_message(client, callback_query):
    message = callback_query.message
    chat_id = message.chat.id
    text = message.text.split('\n\n')[1]  # Mendapatkan pesan rahasia dari teks pesan

    # Hanya pengguna dan pengguna target yang dapat melihat pesan rahasia
    if callback_query.from_user.username == text.split(' ')[1][1:]:
        app.send_message(chat_id, f"Ini pesan rahasiamu:\n\n{text}")
    else:
        app.send_message(chat_id, "Anda tidak memiliki akses untuk membuka pesan rahasia ini.")
