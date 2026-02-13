import os
import telebot
from groq import Groq

# Load tokens from Render environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

def ask_groq(prompt):
    """Send user message to Groq Llama3 model and return the response."""
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message["content"]

@bot.message_handler(func=lambda m: True)
def reply(message):
    user_text = message.text
    try:
        answer = ask_groq(user_text)
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, "Error: Unable to get response from AI.")
        print("Error:", e)

bot.polling()
