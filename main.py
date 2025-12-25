import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

ESVITLO_USERNAME = "esvitlo_kyiv_oblast"

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage)
async def debug_all(event):
    chat = await event.get_chat()
    title = getattr(chat, "title", "")
    username = getattr(chat, "username", "")
    chat_id = getattr(chat, "id", None)
    text = (event.raw_text or "")[:80].replace("\n", " ")

    print("MSG | id=", chat_id, "| user=", username, "| title=", title[:40], "| text=", text)

async def runner():
    me = await client.get_me()
    print("Userbot running as", me.id, me.username)
    while True:
        try:
            await client.run_until_disconnected()
        except Exception as e:
            print("Disconnected with error:", repr(e))
            await asyncio.sleep(5)
            print("Reconnecting...")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(runner())
