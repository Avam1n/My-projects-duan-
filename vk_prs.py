import re
import time
import vk
import logging
from config import Token_VK_not_my

session = vk.Session(Token_VK_not_my)
vk_api = vk.API(session, v="5.131")


class ParsVk:
    url = ''
    list_users = []
    list_users_copy = []

    def __init__(self, url):
        self.url = url

    def req_url(self) -> [list, str]:
        """Этот метод для того, чтобы определить и "взять" нужные нам ID из ссылки. """
        try:
            req = re.search(r'((?P<id1>-?\d+)_(?P<id2>\d+))', self.url)
            own_id = int(req['id1'])
            it_id = int(req['id2'])

            offset_likes = 0

            while True:
                time.sleep(0.6)
                check_list = vk_api.likes.getList(type='post',
                                                  owner_id=own_id,
                                                  item_id=it_id,
                                                  extended=1,
                                                  offset=offset_likes,
                                                  count=1000)

                self.list_users = vk_api.users.get(user_ids=[item['id'] for item in check_list['items'] if
                                                             item.get('is_closed') is not True and item.get(
                                                                 'deactivated') != 'deleted' and item.get(
                                                                 'deactivated') != 'banned'],
                                                   fields='city')  # Создаем список содержащий расширенную информацию о пользователе(интересует 'city' по этому в fields добавили 'city')
                offset_likes += 1000

                if len(self.list_users) != 0:
                    for i in self.list_users:
                        self.list_users_copy.append(i)
                else:
                    break

            return self.list_users_copy
        except Exception as err:
            logging.error(f'{err}')
            return f'Oops!\nЧто-то случилось с парсингом!'

    def show_file(self):  # Реализуем показ нужной нам информации.
        try:
            list_user = ParsVk.req_url(self)
            with open(r'All_open_acc.html', 'w', encoding='UTF-8') as file:
                count = 1
                for element in list_user:
                    element_with_city_item = element.get('city', f'{"-------"}')
                    print(
                        f"-{count}-"
                        f"||ID: {element.get('id'):<10} "
                        f"||Name: {element.get('first_name'):<15} "
                        f"||Last_name: {element.get('last_name'):<20} "
                        f"||City: --{element_with_city_item['title'] if element_with_city_item is not str(element_with_city_item) else element_with_city_item:<18} "
                        f"||Link:   <a href='https://vk.com/id{element.get('id')}'>https://vk.com/id{element.get('id')}</a>" + "<br>",
                        file=file)  # Настроили то как будет выглядеть информация в файле.
                    count += 1
            return file
        except Exception as err:
            logging.error(f'{err}')
            return f'Oops!\nЧто-то пошло не так с созданием файла.'


if __name__ == '__main__':
    play_pars = ParsVk()
    play_pars.show_file()
