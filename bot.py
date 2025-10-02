import telebot
import requests
import os

# токены будут храниться в Render (безопаснее)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def ask_hf(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()[0]["generated_text"]
    except:
        return "⚠️ Ошибка: не удалось получить ответ."

@bot.message_handler(func=lambda message: True)
def reply(message):
    answer = ask_hf(message.text)
    bot.reply_to(message, answer)

print("🤖 Кир запущен…")
bot.polling()
