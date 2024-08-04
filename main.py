import os
import secrets
import utils

import telebot

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TG_TOKEN")
chat_bot_id = int(os.getenv("CHAT_BOT_ID"))
user_id = os.getenv("USER_ID")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["get_quote"])
def get_quote():
    quotes = utils.get_quotes()
    num = secrets.SystemRandom().randint(0, len(quotes) - 1)
    quote = quotes[num]
    for ch in [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]:
        quote = ("\\" + ch).join(quote.split(ch))
    quote = ("\n>").join(quote.split("\n"))
    bot.send_message(
        chat_bot_id, "*Цитата/Мысль\ дня*:\n" + ">" + quote, parse_mode="MarkdownV2"
    )


@bot.message_handler(commands=["healthcheck"])
def healthcheck(message):
    bot.send_message(message.chat.id, "Я живой!")


if __name__ == "__main__":
    get_quote()
