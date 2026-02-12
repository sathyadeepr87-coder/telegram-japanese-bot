from telegram.ext import ApplicationBuilder, MessageHandler, filters
from huggingface_hub import InferenceClient
import os

# Telegram bot token
TELEGRAM_TOKEN = "8190871984:AAGuEQHDLri1luuj1Z0_y9-YTplj0pk35h8"

# HuggingFace API token
os.environ["HF_TOKEN"] = "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"

# Free model (good for Japanese)
client = InferenceClient(
    model="Qwen/Qwen2.5-7B-Instruct",
    token=os.environ["HF_TOKEN"]
)

SYSTEM_PROMPT = """
You are a friendly Japanese tutor.
- Explain grammar simply.
- Provide romaji + kana + English meaning.
- Correct mistakes gently.
- Give 2–3 example sentences.
- Keep explanations short.
"""

async def handle_message(update, context):
    user_text = update.message.text

    response = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        max_tokens=300
    )

    reply = response.choices[0].message["content"]
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
