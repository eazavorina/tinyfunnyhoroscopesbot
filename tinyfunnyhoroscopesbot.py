from flask import Flask, request
from huitoken import token, hook
import telebot
from telebot import types
import random

URL = 'https://api.telegram.org/bot' + token + '/'
pa_url = 'https://whatwhatwhat.pythonanywhere.com/' + hook

bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()

bot.set_webhook(url=pa_url)

app = Flask(__name__)

first = ['День будет относительно успешным.', 'Впереди довольно приятные сутки.', 'Сегодня звёзды не приготовили больших неприятностей.']
second = ['Что бы ни случилось, вас ожидает подъём в', 'Также в ближайшее время вас ждёт успешный период в', 'Вы находитесь на самом пороге прорыва в']
second_add = ['покупке ослов.', 'закатывании огурцов.', 'пинании пенисов.', 'созерцании пупка.']
third = ['Однако будьте осторожны с', 'Следует поаккуратничать с', 'Вас может удивить столкновение с']
third_add = ['ретроградно настроенными соседями.', 'незакрытой ванной ночью.', 'голубями, которые каркают, как вороны.', 'ребёнком в углу позади вас.']
final = ['Устыдитесь же дел своих!', 'Покайтесь же, пока не поздно!', 'Враг не пройдёт!', 'Победа будет за вами!', 'Да будут услышаны ваши молитвы!']

@app.route(f'/{hook}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() in ['привет', 'здравствуй', 'здравствуйте']:
        bot.send_message(message.from_user.id, 'Здравствуйте, дорогуша.')
    elif message.text.lower() == 'гороскоп':
        bot.send_message(message.from_user.id, 'Сейчас расскажу вам странненький гороскоп.')
        znak = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
        keyboard = types.InlineKeyboardMarkup()
        button_list = [types.InlineKeyboardButton(text=x, callback_data='zodiac') for x in znak]
        keyboard.add(*button_list)
        bot.send_message(message.from_user.id, 'Нажмите на ваш знак Зодиака.', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Непонятно! Скажите лучше Гороскоп!')

@bot.callback_query_handler(func=lambda call: call.data == 'zodiac')
def callback_worker(call):
    if call.data == 'zodiac':
        msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third) + ' ' + random.choice(third_add) + ' ' + random.choice(final)
        keyboard = types.InlineKeyboardMarkup()
        thanks = types.InlineKeyboardButton(text = 'Спасибо!', callback_data='thanks')
        keyboard.add(thanks)
        bot.send_message(call.message.chat.id, msg, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'thanks')
def callback_worker(call):
    if call.data == 'thanks':
        msg1 = 'Может, ещё один гороскоп?'
        keyboard = types.InlineKeyboardMarkup()
        onemore = types.InlineKeyboardButton(text='А давай!', callback_data='onemore')
            # И добавляем кнопку на экран
        keyboard.add(onemore)
        nomore = types.InlineKeyboardButton(text='Нет, спасибо', callback_data='nomore')
        keyboard.add(nomore)
            # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(call.message.chat.id, text = msg1, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['onemore', 'nomore'])
def callback_worker(call):
    if call.data == 'onemore':
        msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third) + ' ' + random.choice(third_add) + ' ' + random.choice(final)
        keyboard = types.InlineKeyboardMarkup()
        thanks = types.InlineKeyboardButton(text = 'Спасибо!', callback_data='thanks')
        keyboard.add(thanks)
        bot.send_message(call.message.chat.id, msg, reply_markup=keyboard)
    elif call.data == "nomore":
        keyboard = types.InlineKeyboardMarkup()
        yep = types.InlineKeyboardButton(text='Да, уже хочу', callback_data='yep')
            # И добавляем кнопку на экран
        keyboard.add(yep)
        nope = types.InlineKeyboardButton(text='Нет, давай лучше ещё гороскоп', callback_data='nope')
        keyboard.add(nope)
            # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(call.message.chat.id, text="Хотите знать, почему все гороскопы так похожи?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['yep', 'nope'])
def callback_worker(call):
    if call.data == 'nope':
        msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third) + ' ' + random.choice(third_add) + ' ' + random.choice(final)
        keyboard = types.InlineKeyboardMarkup()
        thanks = types.InlineKeyboardButton(text = 'Спасибо!', callback_data='thanks')
        keyboard.add(thanks)
        bot.send_message(call.message.chat.id, msg, reply_markup=keyboard)
    elif call.data == "yep":
        keyboard = types.InlineKeyboardMarkup()
        link = types.InlineKeyboardButton(text='Эффект Барнума (статья)', url='https://ru.wikipedia.org/wiki/%D0%AD%D1%84%D1%84%D0%B5%D0%BA%D1%82_%D0%91%D0%B0%D1%80%D0%BD%D1%83%D0%BC%D0%B0')
            # И добавляем кнопку на экран
        keyboard.add(link)
        link2 = types.InlineKeyboardButton(text='Эффект Барнума (видео)', url='https://youtu.be/P3RpRH_iVxA')
        # И добавляем кнопку на экран
        keyboard.add(link2)
        bot.send_message(call.message.chat.id, text="Можете посмотреть или почитать по ссылкам!", reply_markup=keyboard)


