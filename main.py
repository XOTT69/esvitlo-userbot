import os
import asyncio
import random
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

BOT_TOKEN = os.environ["BOT_TOKEN"]          # 8413003519:...
TARGET_CHAT_ID = os.environ["TARGET_CHAT_ID"]  # -100...

ESVITLO_CHANNEL = "esvitlo_kyiv_oblast"

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


def send_via_bot(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TARGET_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        r = requests.post(url, data=data, timeout=10)
        print("Bot API status:", r.status_code, r.text[:200])
    except Exception as e:
        print("Bot API error:", e)


@client.on(events.NewMessage(chats=ESVITLO_CHANNEL))
async def esvitlo_handler(event):
    text = event.raw_text or ""

    # тільки підгрупа 2.2
    if "2.2" not in text and "підгрупа 2.2" not in text:
        return

    await asyncio.sleep(random.randint(5, 60))  # антиспам

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    date_line = next(
        (l for l in lines if any(c.isdigit() for c in l) and "." in l),
        ""
    )
    group_lines = [l for l in lines if "2.2" in l]

    body = "\n".join(group_lines) if group_lines else text

    msg = "🔌 <b>Чабани, підгрупа 2.2 (єСвітло)</b>\n"
    if date_line:
        msg += f"📅 {date_line}\n\n"
    else:
        msg += "\n"
    msg += body

    send_via_bot(msg)
    print("Forwarded 2.2 via Bot API")


async def main():
    me = await client.get_me()
    print("Userbot running as", me.id, me.username)
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
