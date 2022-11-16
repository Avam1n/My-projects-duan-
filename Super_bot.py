# from Mydb import Table
import asyncio
import os
import random
import time
import telebot
import vk
import config
import logging
import send_emile
from googletrans import Translator
from telebot import types, TeleBot
from textblob import TextBlob
from vk import exceptions
from vk_prs import ParsVk
from check_active import main

bot: TeleBot = telebot.TeleBot(config.Token)
# db = Table()

logging.basicConfig(level=logging.INFO,
                    filename="mylog.log",
                    filemode="w",
                    format="%(asctime)-15s - %(pathname)s - %(funcName)-8s: Line: %(lineno)d.(%(message)s)",
                    datefmt='%d-%b-%y %H:%M:%S')

stick = {'hi': 'CAACAgIAAxkBAAEEh6diYacMLoyQdAIwEcTu9spC_IzwVAACKgAD78MbMnp5qWur76SZJAQ',
         'think': 'CAACAgIAAxkBAAEErsJieD7Oax4LPgsOg-DPmpsg7xXnEwACIhMAAl1scEuuLYe9O-OAPiQE',
         'you_good': 'CAACAgIAAxkBAAEErshieD9_1LBIHCxCztHT9gfPlNU7PAACfRMAAqN3qEvCWDsDiG_N4CQE',
         'oh_my': 'CAACAgIAAxkBAAEErtNieEHb4YErLRAV7IaVo3lruKSUzQACYhEAApOEmEnCDV-VWpFuAyQE',
         'im_god': 'CAACAgIAAxkBAAEErtVieEIvVxOeHVVAF7JeeZAonNVmCAACPgAD78MbMqgqgDn40xkAASQE',
         }

helper = {'helping': ',я научился собирать незначительную информацию по посту в VK, еще я могу определить '
                     'ТОП активных пользователей паблика нажми кнопку "Pars" и попробуй!'}


@bot.message_handler(commands=['start'])
def start_bot(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                         input_field_placeholder=f"\"Как дела?\"")
    button = types.KeyboardButton("Help!")
    button_prs = types.KeyboardButton("Pars")
    keyboard.add(button, button_prs)
    bot.send_sticker(message.chat.id, f"{stick['hi']}")
    bot.send_message(message.chat.id,
                     "Меня зовут - {0.first_name}!".format(bot.get_me()),
                     reply_markup=keyboard)


"""Со временем реализую подписку на Бота."""


# async def subscribe(message: types.Message):
#     if not db.subscriber_exist(message.from_user.id):
#         print(db.subscriber_exist(message.from_user.id))
#         db.add_subscriber(message.from_user.id)
#     else:
#         db.update_subscription(message.from_user.id, subscription_status=True)
#     bot.send_message(message.chat.id, "Вы успешно подписались на меня.")
#
#
# @bot.message_handler(commands=['subscribe'])
# def start_subscribe(message: types.Message):
#     asyncio.run(subscribe(message))
#
#
# async def unsubscribe(message: types.Message):
#     if not db.subscriber_exist(message.from_user.id):
#         db.add_subscriber(user_id=message.from_user.id, subscription_status=False)
#         bot.send_message(message.chat.id, "Вы итак не подписались на меня.(((")
#     else:
#         db.update_subscription(message.from_user.id, subscription_status=False)
#         bot.send_message(message.chat.id, "Как жаль, что Вы отписались от меня.(((")
#
#
# @bot.message_handler(commands=['unsubscribe'])
# def start_unsubscribe(message: types.Message):
#     asyncio.run(unsubscribe(message))
#

@bot.message_handler(
    regexp='^(Кк[?]ак дела[?]{1})?(как [а-я]{0,4})?(дела[?]{0,1})?$')
def answer_to_question(message):
    """Примитивный диалог, в скором времени буду стараться лучше:-)"""
    answer = bot.send_message(message.chat.id, "Я отлично, сам ты как???")
    bot.register_next_step_handler(answer, answer_q)


@bot.message_handler(content_types=['text'])
def dialog(message):
    match message.text.lower():
        case 'help!':
            bot.send_sticker(message.chat.id, f"{stick['oh_my']}")
            bot.send_message(message.chat.id, "{0.first_name} {1}".format(message.from_user, helper['helping']))
        case 'pars':
            match message.from_user.id in config.list_id:
                case True:
                    inline_keyboard = types.InlineKeyboardMarkup(row_width=3)

                    button_go = types.InlineKeyboardButton('Пост', callback_data='start')
                    button_stop = types.InlineKeyboardButton('Стоп', callback_data='stop')
                    button_active_users = types.InlineKeyboardButton('Группа',
                                                                     callback_data='Active users')
                    inline_keyboard.add(button_go, button_active_users)
                    inline_keyboard.add(button_stop)
                    bot.send_message(message.chat.id, "Подготовь ссылку на пост...\n"
                                                      "(Чтобы начать нажми ⏩⏩ 'По посту')\n"
                                                      "(Для отмены нажми ⏩⏩ 'Стоп')\n"
                                                      "Чтобы получить ТОП-50 активных юзеров по группе юзай: "
                                                      "'Группа'", reply_markup=inline_keyboard)
                case False:
                    bot.send_message(message.chat.id,
                                     f'Прошу прощения, {message.from_user.first_name}, эта функция еще тестируется.\n'
                                     f'Вы сможете ей воспользоваться в скором времени. Приношу свои извинения.')


def answer_q(message):
    """Этот метод нужен для определения эмоции пользователя.
    Переводим для библиотеки с русского на английский, после чего определяем настроение."""
    try:
        msg = message.text
        translator = Translator()
        translation = translator.translate(msg, src='ru', dest='en')
        analysis_polarity = TextBlob(translation.text).polarity
        if analysis_polarity == 1:
            bot.send_message(message.chat.id, "Ого, я очень рад за тебя, {0.first_name}! :-)".format(message.from_user))
        elif 1 > analysis_polarity >= 0.5:
            bot.send_message(message.chat.id,
                             "Это не ПРЕВОСХОДНО, но тем не менее жить с этим можно, {0.first_name}. "
                             "Не отчаивайся!".format(message.from_user))
        elif 0.5 > analysis_polarity >= 0:
            bot.send_message(message.chat.id,
                             "Надеюсь это не выбьет тебя из колеи, {0.first_name}"
                             "Не отчаивайся!".format(message.from_user))
        else:
            bot.send_message(message.chat.id,
                             "В скором времени все наладится, я в это верю и ты, {0.first_name}, "
                             "верь вместе со мной.".format(message.from_user))
    except Exception as err:
        logging.error(f'{err}')
        send_emile.main(message.text)
        bot.send_message(message.chat.id, "Я не совсем понял, что ты имеешь ввиду, но хочу верить, что все хорошо.")


def inline_():
    inline_keyboard = types.InlineKeyboardMarkup(row_width=3)
    button_100 = types.InlineKeyboardButton('По 100 постам', callback_data='button_100')
    button_500 = types.InlineKeyboardButton('По 500 постам', callback_data='button_500')
    button_all_posts = types.InlineKeyboardButton('Вся группа', callback_data='all')
    button_stop = types.InlineKeyboardButton('Стоп', callback_data='stop')
    inline_keyboard.add(button_100, button_500)
    inline_keyboard.add(button_all_posts)
    inline_keyboard.add(button_stop)
    return inline_keyboard


def inline_2():
    inline_keyboard = types.InlineKeyboardMarkup(row_width=3)
    button_go = types.InlineKeyboardButton('Пост', callback_data='start')
    button_stop = types.InlineKeyboardButton('Стоп', callback_data='stop')
    button_active_users = types.InlineKeyboardButton('Группа', callback_data='Active users')
    inline_keyboard.add(button_go, button_stop)
    inline_keyboard.add(button_active_users)
    return inline_keyboard


def inline_3():
    inline_keyboard = types.InlineKeyboardMarkup(row_width=3)
    button_stop = types.InlineKeyboardButton('Стоп', callback_data='stop')
    inline_keyboard.add(button_stop)
    return inline_keyboard


def bot_send():
    say_some = {1: 'Каких камней не бывает в речке?',
                2: 'На столе лежат две монеты, в сумме они дают 3 рубля. Одна из них - не 1 рубль. Какие это монеты?',
                3: 'Что не вместится даже в самую большую кастрюлю?',
                4: 'Что может в одно и то же время стоять и ходить, висеть и стоять, ходить и лежать?',
                5: 'Завязать можно, а развязать нельзя. Что это такое?'}
    return say_some


@bot.message_handler(content_types=['document', 'text'])
def parsing(message):
    try:
        chat_post_parser = ParsVk(message.text)
        chat_post_parser.show_file()
        send_emile.main(message.text)
        bot.send_message(message.chat.id,
                         f'Сейчас попробую скинуть открытые аккаунты в HTML файле:')
        time.sleep(random.randint(2, 5))
        file = open(f'{message.text}.html', 'rb')
        bot.send_document(message.chat.id, file)
        file.close()
        bot.send_message(message.chat.id, f'Вот, что получилось! :-)', reply_markup=inline_2())
        os.remove(f'{message.text}.html')
    except Exception as error:
        logging.error(f'{error}')
        send_emile.main(message.text)
        bot.send_message(message.chat.id, f"Oops! Что-то пошло не так!")


def offset_100(message):
    try:
        bot.send_message(message.chat.id, f'Пока парсим, попробуй отгадать загадку:')
        time.sleep(random.randint(1, 3))
        bot.send_message(message.chat.id, f'{random.choice([value for ket, value in bot_send().items()])}')
        bot.send_message(message.chat.id, f'{main(message.text, 100)}')
        asyncio.run(offset_function(message))
    except vk.exceptions.VkAPIError as err:
        logging.error(f'{err}')
        send_emile.main(message.text)
        mess_from_user_time = bot.send_message(message.chat.id,
                                               'Произошла ошибка, проверь правильность введенных данных.',
                                               reply_markup=inline_())
        bot.register_next_step_handler(message=mess_from_user_time,
                                       callback=dialog)


def offset_500(message):
    try:
        bot.send_message(message.chat.id, f'Пока парсим, попробуй отгадать загадку:')
        time.sleep(random.randint(1, 3))
        bot.send_message(message.chat.id, f'{random.choice([value for ket, value in bot_send().items()])}')
        bot.send_message(message.chat.id, f'{main(message.text, 500)}')
        asyncio.run(offset_function(message))
    except vk.exceptions.VkAPIError as err:
        logging.error(f'{err}')
        send_emile.main(message.text)
        mess_from_user_time = bot.send_message(message.chat.id,
                                               'Произошла ошибка, проверь правильность введенных данных.',
                                               reply_markup=inline_())
        bot.register_next_step_handler(message=mess_from_user_time,
                                       callback=dialog)


def offset_all(message):
    try:
        bot.send_message(message.chat.id, f'Пока парсим, попробуй отгадать загадку:')
        time.sleep(random.randint(1, 3))
        bot.send_message(message.chat.id, f'{random.choice([value for ket, value in bot_send().items()])}')
        bot.send_message(message.chat.id, f'{main(message.text, 0)}')
        asyncio.run(offset_function(message))
    except vk.exceptions.VkAPIError as err:
        logging.error(f'{err}')
        send_emile.main(message.text)
        mess_from_user_time = bot.send_message(message.chat.id,
                                               'Произошла ошибка, проверь правильность введенных данных.',
                                               reply_markup=inline_())
        bot.register_next_step_handler(message=mess_from_user_time,
                                       callback=dialog)


@bot.message_handler(content_types=['document', 'text'])
async def offset_function(message):
    try:
        send_emile.main(message.text)
        await asyncio.sleep(random.randint(2, 5))
        active_users_file = open(f'{message.text}.html', 'rb')
        bot.send_document(message.chat.id, active_users_file)
        active_users_file.close()
        mess = bot.send_message(message.chat.id, f'Продолжим...', reply_markup=inline_())
        bot.register_next_step_handler(mess, callback=dialog)
        os.remove(f'{message.text}.html')
    except Exception as error:
        logging.error(f'{error}')
        send_emile.main(message.text)
        bot.send_message(message.chat.id, f"Oops! Что-то пошло не так!")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Привязываем функционал инлайн-кнопке. """
    try:
        match call.data:
            case 'stop':
                mess_from_user_stop = bot.send_message(call.message.chat.id, 'Стоп, так стоп!', reply_markup=None)
                bot.register_next_step_handler(message=mess_from_user_stop, callback=dialog)
                list_func = [offset_100, offset_500, offset_all]
                exit(i for i in list_func)
            case 'start':
                mess_from_user_start = bot.edit_message_text(chat_id=call.message.chat.id,
                                                             message_id=call.message.message_id,
                                                             text='Давай ссылку на пост!', reply_markup=inline_2())
                bot.register_next_step_handler(message=mess_from_user_start, callback=parsing)
            case 'Active users':
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Введи ID группы. \n'
                                           '(пример:\'cybersportby\' или \'78017410\')', reply_markup=inline_())
            case 'button_100':
                mess_from_user_time = bot.send_message(chat_id=call.message.chat.id,
                                                       text='Примерное время ожидания 3 минуты!',
                                                       reply_markup=inline_3())
                bot.register_next_step_handler(message=mess_from_user_time,
                                               callback=offset_100)
            case 'button_500':
                mess_from_user_time = bot.send_message(chat_id=call.message.chat.id,
                                                       text='Примерное время ожидания 6 минут!',
                                                       reply_markup=inline_3())
                bot.register_next_step_handler(message=mess_from_user_time,
                                               callback=offset_500)
            case 'all':
                mess_from_user_time = bot.send_message(chat_id=call.message.chat.id,
                                                       text='Примерное время ожидания \'ОЧЕНЬ МНОГО\''
                                                            'минут!(зависит от количества постов'
                                                            'в группе)',
                                                       reply_markup=inline_3())
                bot.register_next_step_handler(message=mess_from_user_time,
                                               callback=offset_all)
    except Exception as error:
        logging.error(f'{error}')
        send_emile.main('Ошибка в call')


if __name__ == '__main__':
    try:
        logging.info(f'Bot - started!')
        bot.infinity_polling(non_stop=True, interval=1)
    except Exception as error:
        logging.error(f'{error}')
        send_emile.main('Ошибка в ексепшене(инфинити поллинг!)')
        bot.infinity_polling(non_stop=True, interval=1)
