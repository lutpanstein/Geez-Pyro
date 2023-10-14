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

# Fungsi untuk mengenkripsi pesan
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return b64encode(cipher.encrypt(message))

# Fungsi untuk mendekripsi pesan
def decrypt_message(encrypted_message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(b64decode(encrypted_message)).rstrip(b'\0').decode('utf-8')

# Inisialisasi kunci acak, pastikan kunci ini disimpan dengan aman
key = get_random_bytes(16)

# Fungsi yang akan dijalankan ketika bot menerima pesan
@app.on_message(filters.command("usernamebot", prefixes="@"))
def send_secret_message(client, message: Message):
    try:
        # Split pesan untuk mendapatkan teks pesan dan username target
        _, message_text, target_username = message.text.split(" ", 2)
        
        # Cek apakah username target valid
        if not target_username.startswith("@"):
            raise Exception("Invalid target username")

        # Enkripsi pesan
        encrypted_message = encrypt_message(message_text.encode('utf-8'), key)

        # Kirim pesan terenkripsi ke pengguna target
        client.send_message(target_username, f"🔒 [Pesan Rahasia] 🔒\n\n{b64encode(encrypted_message).decode('utf-8')}")

        # Kirim tombol untuk dekripsi pesan
        message.reply_text(f"🔒 Pesan Rahasia terkirim ke {target_username}! 🔒", reply_markup={
            "inline_keyboard": [
                [{"text": "Buka Pesan Rahasia", "callback_data": b64encode(encrypted_message).decode('utf-8')}]
            ]
        })
    except Exception as e:
        message.reply_text(f"Error: {str(e)}")

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
