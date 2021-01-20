import telebot

from Config import keys, TOKEN
from extensions import ConversionException, MoneyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text='Чтобы начать работу с ботом введите команду в следующем формате:\n<имя переводимой валюты>' \
'<имя валюты в которую нужно перевести>' \
'<количество переводимой валюты>\n для просмотра списка доступных валют введите команду /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Некорректный ввод.')

        quote, base, amoute = values
        total_base = MoneyConverter.get_price(quote, base, amoute)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amoute} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()