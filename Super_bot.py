import telebot
import vk
from vk import exceptions
import config
from telebot import types, TeleBot
import random
from vk_prs import ParsVk
import os
import time
from check_active import main
from textblob import TextBlob
from googletrans import Translator
# from Mydb import Table
import asyncio

bot: TeleBot = telebot.TeleBot(config.Token)
# db = Table()

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

        elif 1 > analysis_polarity >= 0.8:
            bot.send_message(message.chat.id,
                             "Это не ПРЕВОСХОДНО, но тем не менее жить с этим можно, {0.first_name}. "
                             "Не отчаивайся!".format(message.from_user))

        elif 0.8 > analysis_polarity >= 0:
            bot.send_message(message.chat.id,
                             "Это уже что то среднее, правда, {0.first_name}? "
                             "Не отчаивайся!".format(message.from_user))

        else:
            bot.send_message(message.chat.id,
                             "В скором времени все наладится, я в это верю и ты, {0.first_name}, "
                             "верь вместе со мной.".format(message.from_user))
    except Exception as err:
        print(err)
        bot.send_message(message.chat.id, "Я не совсем понял, что ты имеешь ввиду, но хочу верить, что все хорошо.")


def inline_():
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)

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


@bot.message_handler(content_types=['document', 'text'])
def parsing(message):
    try:
        chat_post_parser = ParsVk(message.text)
        chat_post_parser.show_file()

        bot.send_message(message.chat.id,
                         f'Сейчас попробую скинуть открытые аккаунты в HTML файле:')
        time.sleep(random.randint(2, 5))
        file = open(r'All_open_acc.html', 'rb')
        bot.send_document(message.chat.id, file)
        file.close()
        bot.send_message(message.chat.id, f'Вот, что получилось! :-)', reply_markup=inline_2())
        os.remove('All_open_acc.html')
    except Exception as error:
        bot.send_message(message.chat.id,
                         f"Oops! Что-то пошло не так!({error})\n {message.from_user.first_name}, "
                         f"проверь правильность ссылки.")


def offset_100(message):
    try:
        bot.send_message(message.chat.id, f'{main(message.text, 100)}')
        asyncio.run(offset_function(message))
    except vk.exceptions.VkAPIError as err:
        print(err)
        mess_from_user_time = bot.send_message(message.chat.id,
                                               'Произошла ошибка, проверь правильность введенных данных.',
                                               reply_markup=inline_())
        bot.register_next_step_handler(message=mess_from_user_time,
                                       callback=dialog)


def offset_500(message):
    try:
        bot.send_message(message.chat.id, f'{main(message.text, 500)}')
        asyncio.run(offset_function(message))
    except vk.exceptions.VkAPIError as err:
        print(err)
        mess_from_user_time = bot.send_message(message.chat.id,
                                               'Произошла ошибка, проверь правильность введенных данных.',
                                               reply_markup=inline_())

        bot.register_next_step_handler(message=mess_from_user_time,
                                       callback=dialog)


def offset_all(message):
    try:
        bot.send_message(message.chat.id, f'{main(message.text, 0)}')
        asyncio.run(offset_function(message))
    except vk.exceptions.VkAPIError as err:
        print(err)
        mess_from_user_time = bot.send_message(message.chat.id,
                                               'Произошла ошибка, проверь правильность введенных данных.',
                                               reply_markup=inline_())

        bot.register_next_step_handler(message=mess_from_user_time,
                                       callback=dialog)


@bot.message_handler(content_types=['document', 'text'])
async def offset_function(message):
    try:
        bot.send_message(message.chat.id,
                         f'Сейчас попробую скинуть открытые аккаунты в HTML файле:')

        await asyncio.sleep(random.randint(2, 5))
        active_users_file = open(r'Active_users.html', 'rb')
        bot.send_document(message.chat.id, active_users_file)
        active_users_file.close()
        mess = bot.send_message(message.chat.id, f'Продолжим...', reply_markup=inline_())
        bot.register_next_step_handler(mess, callback=dialog)
        os.remove('Active_users.html')
    except Exception as error:
        bot.send_message(message.chat.id,
                         f"Oops! Что-то пошло не так!({error})\n {message.from_user.first_name}, "
                         f"проверь правильность введенных данных.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Привязываем функционал инлайн-кнопке. """
    try:
        match call.data:
            case 'stop':
                mess_from_user_stop = bot.send_message(call.message.chat.id, 'Стоп, так стоп!', reply_markup=None)
                bot.register_next_step_handler(message=mess_from_user_stop, callback=dialog)
            case 'start':
                mess_from_user_start = bot.edit_message_text(chat_id=call.message.chat.id,
                                                             message_id=call.message.message_id,
                                                             text='Давай ссылку на пост!', reply_markup=inline_2())

                # mess_from_user_start = bot.send_message(call.message.chat.id, 'Давай ссылку на пост!')
                bot.register_next_step_handler(message=mess_from_user_start, callback=parsing)
            case 'Active users':
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Введи ID группы. \n'
                                           '(пример:\'cybersportby\' или \'78017410\')', reply_markup=inline_())

            case 'button_100':
                mess_from_user_time = bot.edit_message_text(chat_id=call.message.chat.id,
                                                            message_id=call.message.message_id,
                                                            text='Примерное время ожидания 3 минуты!',
                                                            reply_markup=inline_3())

                bot.register_next_step_handler(message=mess_from_user_time,
                                               callback=offset_100)

            case 'button_500':
                mess_from_user_time = bot.edit_message_text(chat_id=call.message.chat.id,
                                                            message_id=call.message.message_id,
                                                            text='Примерное время ожидания 6 минут!',
                                                            reply_markup=inline_3())

                bot.register_next_step_handler(message=mess_from_user_time,
                                               callback=offset_500)

            case 'all':
                mess_from_user_time = bot.edit_message_text(chat_id=call.message.chat.id,
                                                            message_id=call.message.message_id,
                                                            text='Примерное время ожидания \'ОЧЕНЬ МНОГО\''
                                                                 'минут!(зависит от количества постов'
                                                                 'в группе)',
                                                            reply_markup=inline_3())

                bot.register_next_step_handler(message=mess_from_user_time,
                                               callback=offset_all)

    except Exception as error:
        print(repr(error))
        print(error)


if __name__ == '__main__':
    try:
        bot.infinity_polling(non_stop=True, interval=1)
    except Exception as e:
        print(f'In infinity_polling ====> {e}')
        bot.infinity_polling(non_stop=True, interval=1)
