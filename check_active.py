import time
import vk
from config import Token_VK_not_my

session = vk.Session(Token_VK_not_my)
vk_api = vk.API(session, v="5.131")


class SearchForActive:
    group_id = ''
    dict_posts = {}
    owner_id_list = []
    id_list = []
    favorite_users = []
    favorite_users_dict = {}
    final_dict = {}
    final_str = ''

    def __init__(self, group_id):
        self.group_id = group_id

    def check_group(self):
        """Принимаем и настраиваем на вывод id группы (пример: ввод -->'cybersportby', вывод --> '-78017410').
        Обращаю внимание, что id группы указывается со знаком '-'(минус)"""
        get_group = vk_api.groups.getById(group_id=self.group_id)
        get_group_id = get_group[0]
        group_id = get_group_id.get('id')
        return f'-{group_id}'

    def check_posts(self):
        """Данный метод нужен для того, чтобы перебрать и взять нужную информацию по ВСЕМ постам группы, и определяем
        самого активного участника.(определение проходит исключительно по лайкам)"""
        checking_posts = vk_api.wall.get(owner_id=SearchForActive.check_group(self),
                                         count=30,
                                         filter='all')['items']

        for post_id in checking_posts:
            self.owner_id_list.append(post_id['owner_id'])
            self.id_list.append(post_id['id'])

        self.dict_posts = dict(
            zip(self.id_list, self.owner_id_list))  # Записываем ID в словарь для дальнейшей работы с ним.

        for key, value in self.dict_posts.items():
            """Усыпляем каждый раз потому что того требует VkAPI."""
            time.sleep(0.2)

            check_list = vk_api.likes.getList(type='post',
                                              owner_id=value,
                                              item_id=key,
                                              extended=0,
                                              count=1000)

            checking_item_list = check_list['items']

            for element in checking_item_list:
                self.favorite_users.append(element)

        for element in self.favorite_users:
            self.favorite_users_dict[element] = self.favorite_users_dict.get(element,
                                                                             0) + 1  # Добавляем колличество раз встречаемых ID.

        max_value = max(self.favorite_users_dict.values())

        self.final_dict = {k: v for k, v in self.favorite_users_dict.items() if
                           v == max_value}  # Определяем максимальное значение ключа и записываем в словарь.

        return self.final_dict


if __name__ == '__main__':
    srch = SearchForActive('cybersportby')
    print(srch.check_posts())
    print(f'--> ID: {srch.check_group()}')
