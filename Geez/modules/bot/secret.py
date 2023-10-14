from pyrogram import Client, filters, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
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
@app.on_inline_query()
async def inline_query_handler(client, inline_query):
    input_content = inline_query.query.lower().strip()
    user = find_user(input_content)

    if user:
        # Jika pengguna ditemukan, kirim pesan dengan tombol inline
        message = encrypt_message("Ini adalah pesan rahasia.", user.username)
        button = InlineKeyboardButton("Buka Pesan", callback_data=f"show_message_{user.id}_{message}")
        reply_markup = InlineKeyboardMarkup([[button]])
        result = InlineQueryResultArticle(
            id=user.id,
            title=user.username,
            input_message_content=InputTextMessageContent(message_text="Pesan rahasia", reply_markup=reply_markup)
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
        decrypted_message = decrypt_message(message, user.username)
        await callback_query.answer(decrypted_message)
