import telebot
import config
from telebot import types
import random
from PARSING.vk_prs import ParsVk
from io import BytesIO

bot = telebot.TeleBot(config.Token)

placeholder = {'rates': 'Спросите про курс...',
               'gas': 'Узнайте цену на бензин...',
               'weather': 'Может о погоде хотели узнать?',
               'how_are_you': 'Спроси "как твои дела?"'
               }

range_placeholder = list(placeholder.values())

stick = {'hi': 'CAACAgIAAxkBAAEEh6diYacMLoyQdAIwEcTu9spC_IzwVAACKgAD78MbMnp5qWur76SZJAQ',
         'think': 'CAACAgIAAxkBAAEErsJieD7Oax4LPgsOg-DPmpsg7xXnEwACIhMAAl1scEuuLYe9O-OAPiQE',
         'you_good': 'CAACAgIAAxkBAAEErshieD9_1LBIHCxCztHT9gfPlNU7PAACfRMAAqN3qEvCWDsDiG_N4CQE',
         'oh_my': 'CAACAgIAAxkBAAEErtNieEHb4YErLRAV7IaVo3lruKSUzQACYhEAApOEmEnCDV-VWpFuAyQE',
         'im_god': 'CAACAgIAAxkBAAEErtVieEIvVxOeHVVAF7JeeZAonNVmCAACPgAD78MbMqgqgDn40xkAASQE',

         }

helper = {'helping': ',я могу показать Вам актуальные данные по валюте.'}

list_id = []


@bot.message_handler(commands=['start'])
def start_bot(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True,
                                         input_field_placeholder=f"{random.choice(range_placeholder)}")
    button = types.KeyboardButton("Help!")
    keyboard.add(button)

    bot.send_sticker(message.chat.id, f"{stick['hi']}")
    bot.send_message(message.chat.id,
                     "Меня зовут - {0.first_name}, я еще не знаю для чего нужен :-(".format(bot.get_me()),
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def dialog(message):
    if message.text.upper().__contains__('КАК') and message.text.upper().__contains__(
            'ДЕЛА') and message.text.upper().__contains__('ТВОИ'):
        answer = bot.send_message(message.chat.id, "Я отлично, сам ты как???")
        bot.register_next_step_handler(answer, answer_q)

    if message.text == 'Help!':
        bot.send_sticker(message.chat.id, f"{stick['oh_my']}")
        choice = bot.send_message(message.chat.id, "{0.first_name} {1}".format(message.from_user, helper['helping']))

    if message.text == 'go':
        url = bot.send_message(message.chat.id, "Кидай ссылку, челик")
        bot.register_next_step_handler(url, parsing)


@bot.message_handler(content_types=['document'])
def parsing(message):
    chat_parser = ParsVk(message.text)
    chat_parser_id_open = chat_parser.create_a_open_list
    chat_parser_id_close = chat_parser.create_a_close_list
    # bot.send_message(message.chat.id, f'Открытые акки:')
    # bot.send_document(message.chat.id, chat_parser_id_close)

    bot.send_message(message.chat.id, f'Закрытые акки:')
    with open(r'E:\Project1\BOTS\Close.txt', 'w') as file:
        for elements in chat_parser_id_close:
            file.write(str(elements) + '\n')
        bot.send_document(message.chat.id, file)


def answer_q(message):
    bot.send_message(message.chat.id, "Надеюсь это не сарказм, {0.first_name}! :-)".format(message.from_user))


if __name__ == '__main__':
    bot.infinity_polling(non_stop=True, interval=0)
