import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome_and_help(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}. \n\nЯ умею считать стоимость кол-во одной \
валюты в другой. \n\nВведите команду в следующем формате:\n'Имя валюты' 'валюта в которую хотите перевести' \
'кол-во переводимой валюты' \n\nДоступные команды: \n/start и /help: выводят эту инструкцию; \n/values: список \
доступных валют.")


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров!')

        quote, base, amount = values
        price = CryptoConverter.convert(quote, base, amount)
        total_base = int(amount) * price
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
