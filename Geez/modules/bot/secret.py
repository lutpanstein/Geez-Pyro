from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from Geez import app

ALPHA = {}

@app.on_inline_query(filters.command("whisper"))
async def inline(_, query):
    global ALPHA
    res = []
    txt = query.query
    if not len(txt.split(None, 1)) == 2:
        return await query.answer(
            results=res,
            cache_time=0
        )
    try:
        tar = int(txt.split()[0])
    except:
        try:
            tar = (await _.get_users(txt.split()[0])).id
        except:
            return await query.answer(
                results=res,
                cache_time=0
            )
    Na = (await _.get_users(tar)).first_name
    whisp = txt.split(None, 1)[1]
    WTXT = f"A whisper has been sent to {Na}.\n\nOnly he/she can open it."
    SHOW = InlineKeyboardMarkup([[InlineKeyboardButton("Whisper ☁️", callback_data=f"{query.from_user.id}_{tar}")]])
    SHOW_ONE = InlineKeyboardMarkup([[InlineKeyboardButton("One Time Whisper ☁️", callback_data=f"{query.from_user.id}_{tar}_one")]])
    res2 = [
        InlineQueryResultArticle(
            title="Whisper",
            description=f"Send a whisper to {Na} !",
            input_message_content=InputTextMessageContent(WTXT),
            reply_markup=SHOW
        ),
        InlineQueryResultArticle(
            title="Whisper",
            description=f"Send one time whisper to {Na} !",
            input_message_content=InputTextMessageContent(WTXT),
            reply_markup=SHOW_ONE
        )
    ]
    await query.answer(
        results=res2,
        cache_time=0
    )
    try:
        ALPHA.pop(f"{query.from_user.id}_{tar}")
    except:
        pass
    ALPHA[f"{query.from_user.id}_{tar}"] = whisp

@app.on_callback_query()
async def cbq(_, q):
    try:
        id = q.from_user.id
        spl = q.data.split("_")
        if id != int(spl[1]):
            return await q.answer("This is not for you baka !", show_alert=True)
        for_search = spl[0] + "_" + spl[1]
        try:
            msg = ALPHA[for_search] 
        except:
            msg = "Error ‼️\n\nWhisper has been deleted from Database !"
        SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("Go Inline ☁️", switch_inline_query_current_chat="")]])
        await q.answer(msg, show_alert=True)
        if spl[2] == "one":
            await q.edit_message_text("Whisper has been read !\n\nPress below button to send whisper !", reply_markup=SWITCH)
    except Exception as e:
        await q.answer(str(e), show_alert=True)


