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

# Dictionary untuk menyimpan pesan terenkripsi
encrypted_messages = {}

# Fungsi yang akan dijalankan ketika bot menerima pesan pribadi
@app.on_message(filters.private)
def handle_private_message(client, message: Message):
    try:
        # Cek apakah pesan dimulai dengan @usernamebot dan memiliki 3 argumen
        if not message.text.startswith("@BabuGeezRobot") or len(message.command) < 3:
            return

        # Split pesan untuk mendapatkan teks pesan dan username/id target
        _, message_text, target_id = message.text.split(" ", 2)
        
        # Cek apakah username/id target valid
        if not target_id.startswith("@") and not target_id.isdigit():
            raise Exception("Invalid target username or user ID")

        # Enkripsi pesan
        encrypted_message = encrypt_message(message_text.encode('utf-8'), key)

        # Simpan pesan terenkripsi
        encrypted_messages[message.chat.id] = encrypted_message

        # Kirim pesan terenkripsi ke pengguna target
        client.send_message(target_id, f"🔒 [Pesan Rahasia] 🔒\n\n{b64encode(encrypted_message).decode('utf-8')}")

        # Kirim pesan ke chat aktif untuk memungkinkan pengguna membuka pesan
        client.send_message(
            chat_id=message.chat.id,
            text=f"🔒 Pesan Rahasia terkirim ke {target_id}! 🔒",
            reply_markup={
                "inline_keyboard": [
                    [{"text": "Buka Pesan Rahasia", "callback_data": "decrypt"}]
                ]
            }
        )
    except Exception as e:
        message.reply_text(f"Error: {str(e)}")

# Fungsi yang akan dijalankan ketika tombol di tekan
@app.on_callback_query()
async def button(bot, update):
    try:
        # Dekripsi pesan ketika tombol ditekan
        encrypted_message = encrypted_messages.get(update.message.chat.id)
        if encrypted_message:
            decrypted_message = decrypt_message(encrypted_message, key)

            # Kirim pesan terdekripsi ke pengguna
            await update.message.reply_text(f"🔓 [Pesan Terbuka] 🔓\n\n{decrypted_message}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

