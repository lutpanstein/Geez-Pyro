from pyrogram import Client, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import InlineQueryResultArticle
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied, PeerIdInvalid

from Geez import app

whispers_data = {}


@app.on_inline_query()
async def answer(_, query):
    sender = query.from_user.id
    query_list = query.query.split(" ")
    if query.query == "":
        await query.answer(results=main, switch_pm_text="🔒 Learn How to send Whispers", switch_pm_parameter="start")
    elif len(query_list) == 1:
        results = await previous_target(sender)
        await query.answer(results, switch_pm_text="🔒 Learn How to send Whispers", switch_pm_parameter="start")
    elif len(query_list) >= 2:
        mentioned_user = query_list[-1]
        try:
            mentioned_user = ast.literal_eval(mentioned_user)
        except (ValueError, SyntaxError):
            pass
        if isinstance(mentioned_user, str) and not mentioned_user.startswith("@"):
            results = await previous_target(sender)
            await query.answer(results, switch_pm_text="🔒 Learn How to send Whispers", switch_pm_parameter="start")
            return
        try:
            target_user = await app.get_users(mentioned_user)
            receiver = target_user.id
            if target_user.last_name:
                name = target_user.first_name + target_user.last_name
            else:
                name = target_user.first_name
            text1 = f"A whisper message to {name}"
            text2 = "Only he/she can open it."
            whispers_data[sender] = {"specific": None, "message": text1, "receiver_id": receiver}
            await query.answer(
                results=[
                    InlineQueryResultArticle(
                        title=text1,
                        input_message_content=InputTextMessageContent(
                            f"A whisper message to {target_user.mention}" + " " + text2),
                        url="https://t.me/StarkBots",
                        description=text2,
                        thumb_url="https://telegra.ph/file/33af12f457b16532e1383.jpg",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "🔐 Show Message 🔐",
                                        callback_data=str([sender, receiver]),
                                    )
                                ]
                            ]
                        ),
                    )
                ],
                switch_pm_text="🔒 Learn How to send Whispers",
                switch_pm_parameter="start"
            )
            await check_for_users(receiver)
        except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid,  IndexError):
            results = await previous_target(sender)
            await query.answer(results, switch_pm_text="🔒 Learn How to send Whispers", switch_pm_parameter="start")

# Metode untuk menangani peristiwa ketika pengguna memilih sebuah hasil
@app.on_chosen_inline_result()
async def chosen_inline_result(_, result):
    if result.query == "":
        return
    sender = result.from_user.id
    specific = result.inline_message_id
    try:
        str_to_list = result.query.split(" ")
        message = " ".join(str_to_list[:-1])
        receiver = str_to_list[-1]
        to_user = await app.get_users(receiver)
        receiver_id = to_user.id
        to_user = to_user.__str__()
        whispers_data[sender] = {"specific": specific, "message": message, "receiver_id": receiver_id}
        await check_for_users([sender, receiver_id])
    except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid, IndexError):
        message = result.query
        whispers_data[sender] = {"specific": specific, "message": message}
        

async def previous_target(sender):
    q = whispers_data.get(sender)
    if q and q.get("receiver_id") is not None:
        target_user = await app.get_users(q["receiver_id"])
        first_name = target_user.first_name
        try:
            last_name = target_user.last_name
            name = first_name + last_name
        except KeyError:
            name = first_name
        text1 = f"A whisper message to {name}"
        text2 = "Only he/she can open it."
        mention = f"[{name}](tg://user?id={q['receiver_id']})"
        results = [
              InlineQueryResultArticle(
                  title=text1,
                  input_message_content=InputTextMessageContent(
                      f"A whisper message to {mention}" + " " + text2),
                  url="https://t.me/StarkBots",
                  description=text2,
                  thumb_url="https://telegra.ph/file/33af12f457b16532e1383.jpg",
                  reply_markup=InlineKeyboardMarkup(
                      [
                          [
                              InlineKeyboardButton(
                                  "🔐 Show Message 🔐",
                                  callback_data=str(data_list),
                              )
                          ]
                      ]
                  ),
              )
        ]
    else:
        results = main
    return results
