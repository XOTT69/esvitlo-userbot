import os
import asyncio
import random
import ssl
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

# TLS / SSL контекст для Railway (SECLEVEL=1)[web:78]
ssl_ctx = ssl.create_default_context()
ssl_ctx.set_ciphers("DEFAULT:@SECLEVEL=1")

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH,
    connection_retries=None,
    timeout=30,
    request_retries=5,
    connection_over_ssl=True,
    ssl=ssl_ctx,
)


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

    # Логуємо все, щоб бачити, що бот живий
    print("MSG from", username or title, ":", text[:80].replace("\n", " "))

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


async def main():
    print("MAIN ASYNC START")
    await client.start()  # конект до Telegram з урахуванням ssl_ctx[web:24][web:26]
    me = await client.get_me()
    print("Userbot running as", me.id, me.username)
    print("RUN UNTIL DISCONNECTED...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    print("MAIN ENTER")
    try:
        client.loop.run_until_complete(main())
    except Exception as e:
        import traceback
        print("FATAL ERROR IN MAIN:", repr(e))
        traceback.print_exc()
