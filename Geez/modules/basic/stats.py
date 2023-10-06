"""
if you can read this, this meant you use code from Geez | Ram Project
this code is from somewhere else
please dont hestitate to steal it
because Geez and Ram doesn't care about credit
at least we are know as well
who Geez and Ram is


kopas repo dan hapus credit, ga akan jadikan lu seorang developer

YANG NYOLONG REPO INI TRUS DIJUAL JADI PREM, LU GAY...
©2023 Geez | Ram Team
"""

from datetime import datetime
from pyrogram import Client, enums, errors
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import Message
from geezlibs.geez import geez
from Geez.modules.basic import add_command_help
from Geez.modules.basic.profile import extract_user
from Geez import cmds

@geez("stats", cmds)
async def stats(client: Client, message: Message):
    target_user = await extract_user(message)  # Mendapatkan username atau user ID dari pesan

    try:
        target_user = int(target_user)
    except ValueError:
        try:
            target_user = await client.get_users(target_user)
            target_user = target_user.id
        except Exception as e:
            await message.edit_text(f"`Gagal mendapatkan informasi akun target. Error: {e}`")
            return

    Man = await message.edit_text(f"`Mengambil info akun {target_user} ...`")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0

    try:
        target_user = int(target_user)
        target_user_info = await client.get_chat(target_user)
    except ValueError:
        try:
            user = await client.get_users(target_user)
        except errors.exceptions.bad_request_400.UsernameNotOccupied:
            # Tangani kasus ketika pengguna tidak ditemukan
            target_user_info = target_user
        except Exception as e:
            # Tangani kasus kesalahan umum lainnya
            await message.edit_text(f"Gagal mendapatkan informasi akun target. Error: {e}")
            return

    group_info = []

    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
        elif dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            group_info.append((dialog.chat.id, dialog.chat.title))

            if dialog.chat.type == enums.ChatType.SUPERGROUP:
                sg += 1

                try:
                    # Memeriksa apakah pengguna adalah anggota dari supergrup
                    await client.search_messages(dialog.chat.id, target_user_info.id)
                    user_s = await dialog.chat.get_member(target_user_info.id)

                    if user_s.status in (enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR):
                        a_chat += 1
                except ChatAdminRequired:
                    pass
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1

    group_info = group_info[:20]
    end = datetime.now()
    ms = (end - start)
    group_info_text = "\n".join([f"{id}: {title}" for id, title in group_info])

    await Man.edit_text(
        f"""`Status akun {target_user}, berhasil diambil dalam {ms} detik`
        ` {u} Pesan Pribadi.`
        `berada di {g} Groups.`
        `berada {sg} Super Groups.`
        `berada {c} Channels.`
        `menjadi admin di {a_chat} Chats.`
        `Bots = {b}`
        `Info Grup:\n{group_info_text}`"""
        )

add_command_help(
    "stats",
    [
        [f"{cmds}stats", "Mengambil info akun anda."],
        [f"{cmds}stats @username atau user_id", "Mengambil info akun pengguna lain."],
    ],
)
