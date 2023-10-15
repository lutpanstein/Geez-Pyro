from pyrogram import Client, filters, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, ChosenInlineResult
import hashlib
from Geez import app


# Fungsi untuk mengenkripsi pesan
def encrypt_message(message, username):
    key = f"{app.get_me().id}:{username}"
    encrypted_message = hashlib.sha256(key.encode() + message.encode()).hexdigest()
    return encrypted_message

# Fungsi untuk mendekripsi pesan
def decrypt_message(encrypted_message, username):
    key = f"{app.get_me().id}:{username}"
    decrypted_message = hashlib.sha256(key.encode() + encrypted_message.encode()).hexdigest()
    return decrypted_message

# Fungsi untuk mencari pengguna berdasarkan username/id
def find_user(query):
    try:
        user = app.get_users(query)
        return user
    except Exception as e:
        print(e)
        return None

# Fungsi untuk menangani inline query
@app.on_chosen_inline_result()
async def chosen_inline_result_handler(client, chosen_inline_result):
    if chosen_inline_result.query.startswith("open_whisper"):
        _, user_id, _ = chosen_inline_result.query.split("_")
        user = await app.get_users(int(user_id))
        # Mengirim pesan rahasia hanya ke pengguna yang dituju
        await app.send_message(
            chosen_inline_result.from_user.id,
            "Ini adalah pesan rahasia.",
            reply_markup=InlineKeyboardMarkup([])
        )
        await inline_query.answer([result], cache_time=0)
    else:
        await inline_query.answer([], cache_time=0)

# Fungsi untuk menanggapi tombol inline
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data.startswith("show_message"):
        _, user_id, message = callback_query.data.split("_")
        user = await app.get_users(int(user_id))

    # Meminta input tambahan untuk membuka pesan
        message_button = InlineKeyboardButton(
            "Buka Pesan",
            switch_inline_query=f"open_whisper_{user.id}_"
        )

        reply_markup = InlineKeyboardMarkup([[message_button]])

        decrypted_message = decrypt_message(message, user.username)
        await callback_query.answer(
            decrypted_message,
            reply_markup=reply_markup
        )
