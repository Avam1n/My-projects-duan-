import telebot
import config
from telebot import types
import random
from vk_prs import ParsVk
import os
import time

bot = telebot.TeleBot(config.Token)

# placeholder = {'rates': 'Спросите про курс...',
#                'gas': 'Узнайте цену на бензин...',
#                'weather': 'Может о погоде хотели узнать?',
#                'how_are_you': 'Спроси "как твои дела?"'
#                }

# range_placeholder = list(placeholder.values())

stick = {'hi': 'CAACAgIAAxkBAAEEh6diYacMLoyQdAIwEcTu9spC_IzwVAACKgAD78MbMnp5qWur76SZJAQ',
         'think': 'CAACAgIAAxkBAAEErsJieD7Oax4LPgsOg-DPmpsg7xXnEwACIhMAAl1scEuuLYe9O-OAPiQE',
         'you_good': 'CAACAgIAAxkBAAEErshieD9_1LBIHCxCztHT9gfPlNU7PAACfRMAAqN3qEvCWDsDiG_N4CQE',
         'oh_my': 'CAACAgIAAxkBAAEErtNieEHb4YErLRAV7IaVo3lruKSUzQACYhEAApOEmEnCDV-VWpFuAyQE',
         'im_god': 'CAACAgIAAxkBAAEErtVieEIvVxOeHVVAF7JeeZAonNVmCAACPgAD78MbMqgqgDn40xkAASQE',

         }

helper = {'helping': ',я научился собирать незначительную информацию по посту в VK, нажми кнопку "Pars" и попробуй!'}

list_id = [655226441, 745195390]


@bot.message_handler(commands=['start'])
def start_bot(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                         input_field_placeholder=f"Сcылка из VK...")
    button = types.KeyboardButton("Help!")
    button_prs = types.KeyboardButton("Pars")
    keyboard.add(button, button_prs)

    bot.send_sticker(message.chat.id, f"{stick['hi']}")
    bot.send_message(message.chat.id,
                     "Меня зовут - {0.first_name}!".format(bot.get_me()),
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

    if message.text.lower() == 'pars' and message.from_user.id == message.from_user.id in list_id:
        inline_keyboard = types.InlineKeyboardMarkup(row_width=2)

        button_go = types.InlineKeyboardButton('start', callback_data='start')
        button_stop = types.InlineKeyboardButton('stop', callback_data='stop')

        inline_keyboard.add(button_go, button_stop)
        bot.send_message(message.chat.id, "Подготовь ссылку на пост...\n"
                                          "(Чтобы начать нажми ⏩⏩ 'start')\n"
                                          "(Для отмены нажми ⏩⏩ 'stop')",
                         reply_markup=inline_keyboard)


def answer_q(message):
    bot.send_message(message.chat.id, "Надеюсь это не сарказм, {0.first_name}! :-)".format(message.from_user))


@bot.message_handler(content_types=['document', 'text'])
def parsing(message):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)

    button_go = types.InlineKeyboardButton('start', callback_data='start')
    button_stop = types.InlineKeyboardButton('stop', callback_data='stop')

    inline_keyboard.add(button_go, button_stop)
    try:
        chat_parser = ParsVk(message.text)
        chat_parser_id_open = chat_parser.show_file

        bot.send_message(message.chat.id,
                         f'Сейчас попробую скинуть открытые аккаунты в HTML файле:')
        time.sleep(random.randint(2, 5))
        file = open(r'All_open_acc.html', 'rb')
        bot.send_document(message.chat.id, file)
        file.close()
        bot.send_message(message.chat.id, f'Вот, что получилось! :-)', reply_markup=inline_keyboard)
        os.remove('All_open_acc.html')
    except Exception as err:
        bot.send_message(message.chat.id,
                         f"Oops! Что-то пошло не так!({err})\n {message.from_user.first_name}, "
                         f"проверь правильность ссылки.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Привязываем функционал инлайн-кнопке. """
    try:
        if call.message:
            if call.data == 'stop':
                mess_from_user_stop = bot.send_message(call.message.chat.id, 'Stop, так Stop!')
                bot.register_next_step_handler(message=mess_from_user_stop, callback=dialog)
            elif call.data == 'start':
                mess_from_user_start = bot.send_message(call.message.chat.id, 'Давай ссылку на пост...')
                bot.register_next_step_handler(message=mess_from_user_start, callback=parsing)

    except Exception as err:
        print(repr(err))


if __name__ == '__main__':
    bot.infinity_polling(non_stop=True, interval=0)
