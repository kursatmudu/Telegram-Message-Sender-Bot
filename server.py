import asyncio
from flask import Flask, jsonify, request
from threading import Thread
from rabbitMq import RabbitMQ, MessageQueue, Worker

app                     = Flask(__name__)
rabbitmq                = RabbitMQ()
message_queue           = MessageQueue(rabbitmq)
worker                  = Worker(rabbitmq)

@app.route("/send-message", methods=["POST"])
def send_telegram_message():
    try:
        message                 = request.json
        message_queue.add_message(message)
        return jsonify({"status": "Message added to the queue successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def FlaskSession():
    app.run(host="0.0.0.0", port=1907)

if __name__ =='__main__':
    flask_thread            = Thread(target = FlaskSession)
    flask_thread.start()
    asyncio.run(worker.process_messages())