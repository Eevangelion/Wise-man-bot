import os, json, secrets
import telebot

import gdrive


from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TG_TOKEN")
chat_id = int(os.getenv("CHAT_ID"))
user_id = os.getenv("USER_ID")

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['get_quote'])
def get_quote(message):
    quotes = gdrive.get_quotes()
    num = secrets.SystemRandom().randint(0, len(quotes) - 1)
    quote = quotes[num]
    for ch in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
        quote = ("\\" + ch).join(quote.split(ch))
    quote = ("\n>").join(quote.split('\n'))
    bot.send_message(message.chat.id, '*Цитата\ дня*:\n' + '>' + quote, parse_mode="MarkdownV2")

@bot.message_handler(commands=['add_quote'])
def add_quote(message):
    data = gdrive.get_file_data()
    data['messages'].append({'text': message.text[11:]})
    with open('quotes.json', 'w', encomessageding='utf8') as q:
        json.dump(data, q, indent=4, ensure_ascii=False)

@bot.message_handler(commands=['delete_last'])
def delete_last():
    data = gdrive.get_file_data()
    data['messages'].pop()
    with open('quotes.json', 'w', encoding='utf8') as q:
        json.dump(data, q, indent=4, ensure_ascii=False)

def Run():
    bot.infinity_polling()