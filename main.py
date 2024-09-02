from flask import Flask, request, jsonify
from telegram import Bot
import os

app = Flask(__name__)

# Замените на ваш токен Telegram
#TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
bot = Bot("7321975821:AAHnTgQqv7XeOadbjPUFX1cQzIxRhv3njUQ")

# Словарь для хранения пользовательских ID Telegram и соответствующих Linear ID
user_mapping = {
    # "linear_user_id": "telegram_user_id"
}

@app.route('/webhook', methods=['POST'])
def linear_webhook():
    data = request.json

    # Проверяем событие назначения задачи
    if data['type'] == 'Issue.assigned':
        assignee_id = data['data']['assigneeId']
        issue_title = data['data']['title']
        issue_url = data['data']['url']

        # Если назначенный пользователь есть в нашем маппинге
        if assignee_id in user_mapping:
            telegram_user_id = user_mapping[assignee_id]
            message = f"Вам назначена новая задача: {issue_title}\nСсылка: {issue_url}"
            bot.send_message(chat_id=telegram_user_id, text=message)

    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
