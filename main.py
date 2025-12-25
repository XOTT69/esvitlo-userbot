import os
import asyncio
import random
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

print("PYTHON MAIN STARTED")

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

BOT_TOKEN = os.environ["BOT_TOKEN"]
TARGET_CHAT_ID = os.environ["TARGET_CHAT_ID"]

ESVITLO_USERNAME = "esvitlo_kyiv_oblast"

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


def send_via_bot(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TARGET_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    r = requests.post(url, data=data, timeout=10)
    print("Bot API:", r.status_code, r.text[:200])


@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    username = getattr(chat, "username", "")
    title = getattr(chat, "title", "")
    text = event.raw_text or ""

    # Логуємо ВСЕ, щоб бачити, що бот живий
    print("MSG from", username or title, ":", text[:80].replace("\n", " "))

    # Фільтр по єСвітлу
    if username != ESVITLO_USERNAME:
        return

    if "2.2" not in text and "підгрупа 2.2" not in text:
        return

    await asyncio.sleep(random.randint(5, 60))

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
    print("Forwarded 2.2 to channel")


async def runner():
    print("RUNNER STARTED")
    me = await client.get_me()
    print("Userbot running as", me.id, me.username)
    print("RUN UNTIL DISCONNECTED...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    print("MAIN ENTER")
    client.start()          # ініціалізація клієнта Telethon[web:24]
    client.loop.run_until_complete(runner())
