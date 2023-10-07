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
from pyrogram import Client, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import Message
from geezlibs.geez import geez
from Geez.modules.basic import add_command_help
from Geez.modules.basic.profile import extract_user
from Geez import cmds

@geez("stats", cmds)
async def stats(client: Client, message: Message):
    Man = await message.edit_text("`Mengambil info akun ...`")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh = await client.get_me()

    # List to store information of groups and supergroups
    group_info = []

    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
        elif dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            
            group_info.append((dialog.chat.id, dialog.chat.title))

            if dialog.chat.type == enums.ChatType.SUPERGROUP:
                sg += 1
                user_s = await dialog.chat.get_member(int(Meh.id))
                if user_s.status in (
                    enums.ChatMemberStatus.OWNER,
                    enums.ChatMemberStatus.ADMINISTRATOR,
                ):
                    a_chat += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1

    group_info = group_info[:20]

    end = datetime.now()
    ms = (end - start).seconds

    group_info_text = "\n".join([f"{id}: {title}" for id, title in group_info])

    await Man.edit_text(
        f"""`Status akun anda, berhasil diambil dalam {ms} detik`
        ` {u} Pesan Pribadi.`
        `berada di {g} Groups.`
        `berada {sg} Super Groups.`
        `berada {c} Channels.`
        `menjadi admin di {a_chat} Chats.`
        `Bots = {b}`
        `Info Grup:\n{group_info_text}`"""
    )

@geez(["scan"], cmds)
async def scan(client: Client, message: Message):
    ex = await message.edit_text("`Mengambil info akun target ...`")
    user_id = await extract_user(message)

    # List to store information of groups and supergroups
    group_info = []

    try:
        user = await client.get_users(user_id)

        async for dialog in client.get_dialogs():
            if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
                group_info.append((dialog.chat.id, dialog.chat.title))

        group_info = group_info[:30]

        group_info_text = "\n".join([f"{id}: {title}" for id, title in group_info])

        result = user if isinstance(user, list) and user else None

        await ex.edit(
            f"""<b>Daftar Grup User {user.first_name}:</b>\n\n{group_info_text}""",
            parse_mode=enums.ParseMode.HTML,
        )

    except Exception as e:
        await ex.edit(f"**INFO:** `{e}`")


add_command_help(
    "stats",
    [
        [f"{cmds}stats", "Mengambil info akun anda."],
    ]
)
