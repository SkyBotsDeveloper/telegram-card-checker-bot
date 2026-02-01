from pyrogram import filters
from pyromod import Client
from pyrogram.types import Message
from utilsdf.db import Database
from utilsdf.functions import (
    anti_bots_telegram,
    get_bin_info,
    get_cc,
    antispam,
    get_text_from_pyrogram,
)
from utilsdf.vars import PREFIXES
from gates.astharoth import astharoth
from time import perf_counter


@Client.on_message(filters.command("at", PREFIXES))
async def at(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.is_authorized(user_id, m.chat.id):
            return await m.reply(
                "𝑻𝒉𝒊𝒔 𝒄𝒉𝒂𝒕 𝒊𝒔 𝒏𝒐𝒕 𝒂𝒑𝒑𝒓𝒐𝒗𝒆𝒅 𝒕𝒐 𝒖𝒔𝒆 𝒕𝒉𝒊𝒔 𝒃𝒐𝒕.", quote=True
            )
        user_info = db.get_info_user(user_id)
        is_free_user = user_info["MEMBERSHIP"]
        is_free_user = is_free_user.lower() == "free user"
        if is_free_user:
            captcha = await anti_bots_telegram(m, client)
            if not captcha:
                return
    text = get_text_from_pyrogram(m)
    ccs = get_cc(text)
    if not ccs:
        return await m.reply(
            "𝙂𝙖𝙩𝙚𝙬𝙖𝙮 <code>𝘼𝙨𝙩𝙝𝙖𝙧𝙤𝙩𝙝 -» $0 ♻️</code>\n𝙁𝙤𝙧𝙢𝙖𝙩 -» <code>/at cc|month|year|cvc</code>",
            quote=True,
        )
    ini = perf_counter()
    cc = ccs[0]
    mes = ccs[1]
    ano = ccs[2]
    cvv = ccs[3]

    resp = await get_bin_info(cc[0:6])
    if resp is None:
        return await m.reply(
            "<b>No se encontraron resultados para el bin!</b>", quote=True
        )
    brand = resp["brand"]
    country_name = resp["country_name"]
    country_flag = resp["country_flag"]
    bank = resp["bank"]
    level = resp["level"] if resp["level"] else "UNAVAILABLE"
    typea = resp["type"] if resp["type"] else "UNAVAILABLE"
    banned_bin = resp["banned"]
    rol = user_info["RANK"].capitalize()
    # nick = user_info["NICK"]
    if user_id not in [6473966490, 8088623806] and (
        banned_bin or "prepaid" in level.lower() or "prepaid" in typea.lower()
    ):
        return await m.reply("𝘽𝙞𝙣 -» <code>Banned!</code> ⚠", quote=True)
    # check antispam
    antispam_result = antispam(user_id, user_info["ANTISPAM"], is_free_user)
    if antispam_result != False:
        return await m.reply(
            f"𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩... -» <code>{antispam_result}'s</code>", quote=True
        )
    msg_to_edit = await m.reply("𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩...", quote=True)
    cc_formatted = f"{cc}|{mes}|{ano}|{cvv}"

    status, status1 = await astharoth(cc, mes, ano, cvv)

    final = perf_counter() - ini
    with Database() as db:
        db.increase_checks(user_id)

    text_ = f"""<b>ア 𝘾𝘾 -» <code>{cc_formatted}</code>
カ 𝙎𝙩𝙖𝙩𝙪𝙨 -» <code>{status}</code>
ツ 𝙍𝙚𝙨𝙪𝙡𝙩 -» <code>{status1}</code>

キ 𝘽𝙞𝙣 -» <code>{brand}</code> - <code>{typea}</code> - <code>{level}</code>
朱 𝘽𝙖𝙣𝙠 -» <code>{bank}</code>
零 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 -» <code>{country_name}</code> {country_flag}

⸙ 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 -» <code>𝘼𝙨𝙩𝙝𝙖𝙧𝙤𝙩𝙝 -» $0</code>
꫟ 𝙏𝙞𝙢𝙚 -» <code>{final:0.3}'s</code>
ᥫ᭡ 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝙗𝙮 -» <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a> [{rol}]</b>"""

    await msg_to_edit.edit(text_)
