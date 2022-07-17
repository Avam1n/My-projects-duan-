import re
import time
import vk
from config import Token_VK_not_my

session = vk.Session(Token_VK_not_my)
vk_api = vk.API(session, v="5.131")


class ParsVk:
    url = ''
    list_users = []

    def __init__(self, url):
        self.url = url

    def req_url(self):
        """Этот метод для того, чтобы определить и "взять" нужные нам ID из ссылки. """
        try:
            req = re.search(r'((?P<id1>-?\d+)_(?P<id2>\d+))', self.url)
            own_id = int(req['id1'])
            it_id = int(req['id2'])
            check_list = vk_api.likes.getList(type='post',
                                              owner_id=own_id,
                                              item_id=it_id,
                                              extended=1,
                                              count=1000)
            self.list_users = vk_api.users.get(user_ids=[i['id'] for i in check_list['items']],
                                               fields='city')  # Создаем список содержащий расширенную информацию о пользователе(интересует 'city' по этому в fields добавили 'city')
            return self.list_users
        except Exception as err:
            print(f'{err}-- req_url')
            return f'Oops!\nЧто-то пошло не так... в парсе.'

    def create_a_open_list(self):  # Реализуем создание списка ОТКРЫТЫХ аккаунтов.
        time.sleep(0.3)
        try:
            open_list = ParsVk.req_url(self)
            list_users = []
            for i in open_list:  # В цикле поэлементно проверяем на соответствие желаемому условию.
                if i.get('is_closed') is not True and i.get('deactivated') != 'deleted':
                    list_users.append(i)
            return list_users
        except Exception as err:
            print(f'{err}-- create_a_open_list')
            return f'Oops!\nЧто-то пошло не так... в создании списка.'

    def show_file(self):  # Реализуем показ нужной нам информации.
        try:
            list_user = ParsVk.create_a_open_list(self)
            with open(r'All_open_acc.html', 'w', encoding='UTF-8') as file:
                for element in list_user:
                    element_with_city_item = element.get('city', f'{"-------"}')
                    print(
                        f"||ID: {element.get('id'):<10} "
                        f"||Name: {element.get('first_name'):<15} "
                        f"||Last_name: {element.get('last_name'):<20} "
                        f"||City: --{element_with_city_item['title'] if element_with_city_item is not str(element_with_city_item) else element_with_city_item:<18} "
                        f"||Link:   <a href='https://vk.com/id{element.get('id')}'>https://vk.com/id{element.get('id')}</a>" + "<br>",
                        file=file)  # Настроили то как будет выглядеть информация в файле.
            return file
        except Exception as err:
            print(err)
            return f'Oops!\nЧто-то пошло не так... в отображении.'


if __name__ == '__main__':
    play_pars = ParsVk()
    play_pars.create_a_open_list()
    play_pars.show_file()
    play_pars.req_url()
