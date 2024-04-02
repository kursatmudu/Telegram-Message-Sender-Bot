# Telegram Message Sender Bot

This bot provides a backend using Flask and RabbitMQ to send Telegram messages via a web API. It also includes a worker to handle messages coming from RabbitMQ and deliver them to Telegram.


## Installation 

1. Clone: Clone this repository to your local machine:

```bash 
git clone https://github.com/kursatmudu/Telegram-Message-Sender-Bot.git
```

2. Change Directory: Navigate to the project directory:
```bash
cd Telegram-Message-Sender-Bot
```

3. Install Requirements: Install the required Python packages:
```bash
pip install -r requirements.txt
```

4. Configuration: Edit the `config.yaml` file to set your Telegram API credentials and target channel:
```yaml
  telegram_api_id: YOUR_API_ID
  telegram_api_hash: YOUR_API_HASH
  telegram_user:
      {
      user1: 'telegram_session1',
      user2: 'telegram_session2'
      }
  telegram_target_channel: YOUR_TARGET_CHANNEL
```

5. Run: Start the bot:
```bash
python server.py
```

## Usage

1. Sending Messages: Send a message using the `/send-message` API. Example request:
```http
POST /send-message HTTP/1.1
Content-Type: application/json

{
    "target_channel": "YOUR_TARGET_CHANNEL",
    "message": "This is a test message.",
    "sender": "user1"
}
```

   - `target_channel`: The name of the target channel where the message will be sent.
   - `message`: The text of the message to be sent.
   - `sender`: The username to use for using the Telegram API.

2. Message Processing: After the message is sent, it is processed via RabbitMQ and delivered to your Telegram channel.

3. Note: RabbitMQ and the Flask server must be running for the bot to work. Make sure RabbitMQ server and the Flask application are running successfully.