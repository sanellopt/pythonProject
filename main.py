from cmath import e

import telebot

from config import TOKIN, keys
from utils import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKIN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать конвертацию, введите команду боту в следующем формате: \n<имя валюты>  \
<в какую валюту перевести>  \
<количество переводимой валюты>\nЧтобы увидеть список всех доступных валют, введите команду :\n/values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    global total_base, amount, quote, base
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException(f'Слишком много параметров.')

        quote, base, amount = values
        total_base = CriptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду\n{e}')
    else:
        text = f'цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
