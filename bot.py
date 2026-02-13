import os
import telebot
from groq import Groq

# Load tokens from Render environment variables
TELEGRAM_TOKEN = os.getenv("v("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Safety check: ensure tokens exist
if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN is missing. Add it in Render → Environment.")

if GROQ_API_KEY is None:
    raise ValueError("GROQ_API_KEY is missing. Add it in Render → Environment.")

# Initialize Telegram bot and Groq client
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

def ask_groq(prompt: str) -> str:
    """Send user message to Groq Llama3 model and return the response."""
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message["content"]

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    try:
        reply = ask_groq(user_text)
    except Exception as e:
        reply = f"Error contacting Groq: {e}"

    bot.send_message(message.chat.id, reply)

# Start polling
bot.polling(none_stop=True)

