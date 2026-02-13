import os
import telebot
from groq import Groq

# Load tokens from Render environment variables
TELEGRAM_TOKEN = os.getenv("8190871984:AAGuEQHDLri1luuj1Z0_y9-YTplj0pk35h8")
GROQ_API_KEY = os.getenv("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")

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
