import asyncio, json, pika, pika.exceptions
from telegramServer import Telegram

class RabbitMQ:
    def __init__(self, hostname='localhost'):
        self.hostname = hostname
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.hostname))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='message_queue')

    def disconnect(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def get_channel(self):
        if self.channel and self.channel.is_open:
            return self.channel
        else:
            self.connect()
            return self.channel

class MessageQueue:
    def __init__(self, rabbitmq):
        self.channel = rabbitmq.get_channel()

    def add_message(self, data):
        self.channel.basic_publish(exchange='', routing_key='message_queue', body = json.dumps(data))

class Worker:
    def __init__(self, rabbitmq):
        self.rabbitmq = rabbitmq
        self.telegram = Telegram()

    async def process_messages(self):
        global message_queue
        while True:
            try:
                self.channel = self.rabbitmq.get_channel()
                method_frame, header_frame, body = self.channel.basic_get(queue='message_queue', auto_ack=True)
                if method_frame:
                    data = json.loads(body)
                    target_channel = data["target_channel"]
                    message = data["message"]
                    sender = data["sender"]
                    await self.telegramInitialized(target_channel, message, sender)
                else:
                    await asyncio.sleep(1)
            except pika.exceptions.AMQPError:
                rabbitmq = RabbitMQ()
                message_queue = MessageQueue(rabbitmq)
                
    async def telegramInitialized(self, target_channel, text, session_owner):
        await self.telegram.initialize(session_owner)
        await self.telegram.send_message(target_channel, text)
        await self.telegram.disconnect()