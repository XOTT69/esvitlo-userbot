import asyncio
import os
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]
TARGET_CHAT_ID = int(os.environ["TARGET_CHAT_ID"])

ESVITLO_CHANNEL = "esvitlo_kyiv_oblast"

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


@client.on(events.NewMessage(chats=ESVITLO_CHANNEL))
async def handler(event):
    text = event.raw_text or ""

    # Фільтр тільки по підгрупі 2.2
    if "2.2" not in text and "підгрупа 2.2" not in text:
        return

    # Легкий рандомний ділей, щоб не палитись
    await asyncio.sleep(random.randint(5, 60))

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    date_line = next((l for l in lines if any(c.isdigit() for c in l) and "." in l), "")
    group_lines = [l for l in lines if "2.2" in l]

    body = "\n".join(group_lines) if group_lines else text

    msg = "🔌 Чабани, підгрупа 2.2 (єСвітло)\n"
    if date_line:
        msg += f"📅 {date_line}\n\n"
    else:
        msg += "\n"
    msg += body

    await client.send_message(TARGET_CHAT_ID, msg)
    print("Forwarded 2.2 message")


async def main():
    me = await client.get_me()
    print("Userbot running as", me.id, me.username)
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
