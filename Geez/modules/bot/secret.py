from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from Geez import app


def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return b64encode(cipher.encrypt(message))

# Fungsi untuk mendekripsi pesan
def decrypt_message(encrypted_message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(b64decode(encrypted_message)).rstrip(b'\0').decode('utf-8')

# Inisialisasi kunci acak, pastikan kunci ini disimpan dengan aman
key = get_random_bytes(16)


# Fungsi yang akan dijalankan ketika inline query diterima
@app.on_inline_query()
def inline_query(bot, update):
    try:
        # Cek apakah inline query memiliki cukup argumen
        if len(update.query.split()) < 3:
            return

        # Split inline query untuk mendapatkan teks pesan dan username/id target
        _, message_text, target_id = update.query.split(" ", 2)
        
        # Cek apakah username/id target valid
        if not target_id.startswith("@") and not target_id.isdigit():
            return

        # Enkripsi pesan
        encrypted_message = encrypt_message(message_text.encode('utf-8'), key)

        # Kirim hasil inline query dengan tombol untuk dekripsi pesan
        bot.answer_inline_query(
            update.id,
            results=[
                InlineQueryResultArticle(
                    id='1',
                    title='Klik untuk mengirim pesan rahasia',
                    input_message_content=InputTextMessageContent(
                        message_text=f"🔒 [Pesan Rahasia] 🔒\n\n{b64encode(encrypted_message).decode('utf-8')}"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text='Buka Pesan Rahasia', callback_data=b64encode(encrypted_message).decode('utf-8'))]]
                    )
                )
            ]
        )
    except Exception as e:
        print(f"Error: {str(e)}")

# Fungsi yang akan dijalankan ketika tombol di tekan
@app.on_callback_query()
async def button(bot, update):
    try:
        # Dekripsi pesan ketika tombol ditekan
        encrypted_message = update.data.encode('utf-8')
        decrypted_message = decrypt_message(encrypted_message, key)

        # Kirim pesan terdekripsi ke pengguna
        await update.message.reply_text(f"🔓 [Pesan Terbuka] 🔓\n\n{decrypted_message}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


