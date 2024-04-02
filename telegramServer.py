import asyncio
import yaml
from telethon.sync import TelegramClient as Client

class ClientSelector:
    def __init__(self) -> None:
        self.user_list = []
        self.config = yaml.safe_load(open("config.yaml", "r"))
        self.api_id = self.config["telegram_api_id"]
        self.api_hash = self.config["telegram_api_hash"]
        self.telegram_user = self.config["telegram_user"]
        self.clients = {}

    def getClient(self, session_owner):
        if session_owner not in self.clients:
            self.clients[session_owner] = Client(f"TelegramSessions/{self.telegram_user[session_owner]}", self.api_id, self.api_hash)
        return self.clients[session_owner]

class Telegram:
    def __init__(self):
        self.config             = yaml.safe_load(open("config.yaml", "r"))
        self.api_id             = self.config["telegram_api_id"]
        self.api_hash           = self.config["telegram_api_hash"]
        self.target_channel     = self.config["telegram_target_channel"]
        self.telegram_user      = self.config["telegram_user"]
        self.client             = None
        self.client_selector    = ClientSelector()

    async def initialize(self, session_owner):
        self.client = self.client_selector.getClient(session_owner)
        await self.client.start()

    async def disconnect(self):
        await self.client.disconnect()

    async def send_message(self, target_channel, text):
        await self.client.send_message(target_channel, text, parse_mode="HTML")

    async def get_messages(self):
        while True:
            async for event in self.client.iter_messages(self.target_channel, limit=1):
                message = event.message
                if message == "/balance":
                    return
                await asyncio.sleep(2)