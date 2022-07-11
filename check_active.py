import operator
import time
import vk
from config import Token_VK_not_my
from collections import Counter

session = vk.Session(Token_VK_not_my)
vk_api = vk.API(session, v="5.131")
start_time = time.time()


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
                                         offset=0,
                                         count=20,
                                         filter='all')['items']
        # count_str = 0
        for post_id in checking_posts:
            self.owner_id_list.append(post_id['owner_id'])
            self.id_list.append(post_id['id'])
            # count_str += 1
            # print(f"{count_str} - {post_id}")

        # time.sleep(0.3)
        #
        # checking_posts = vk_api.wall.get(owner_id=SearchForActive.check_group(self),
        #                                  offset=1 * 100,
        #                                  count=100,
        #                                  filter='all')['items']
        #
        # for post_id in checking_posts:
        #     self.owner_id_list.append(post_id['owner_id'])
        #     self.id_list.append(post_id['id'])
        #     # count_str += 1
        #     # print(f"{count_str} - {post_id}")
        #
        # time.sleep(0.3)
        #
        # checking_posts = vk_api.wall.get(owner_id=SearchForActive.check_group(self),
        #                                  offset=2 * 100,
        #                                  count=100,
        #                                  filter='all')['items']
        #
        # for post_id in checking_posts:
        #     self.owner_id_list.append(post_id['owner_id'])
        #     self.id_list.append(post_id['id'])
        #     # count_str += 1
        #     # print(f"{count_str} - {post_id}")
        #
        # time.sleep(0.3)
        #
        # checking_posts = vk_api.wall.get(owner_id=SearchForActive.check_group(self),
        #                                  offset=3 * 100,
        #                                  count=100,
        #                                  filter='all')['items']
        #
        # for post_id in checking_posts:
        #     self.owner_id_list.append(post_id['owner_id'])
        #     self.id_list.append(post_id['id'])
        #     # count_str += 1
        #     # print(f"{count_str} - {post_id}")
        #
        # time.sleep(0.3)
        #
        # checking_posts = vk_api.wall.get(owner_id=SearchForActive.check_group(self),
        #                                  offset=4 * 100,
        #                                  count=100,
        #                                  filter='all')['items']
        #
        # for post_id in checking_posts:
        #     self.owner_id_list.append(post_id['owner_id'])
        #     self.id_list.append(post_id['id'])
        #     # count_str += 1
        #     # print(f"{count_str} - {post_id}")
        #
        # time.sleep(0.3)
        #
        # checking_posts = vk_api.wall.get(owner_id=SearchForActive.check_group(self),
        #                                  offset=5 * 100,
        #                                  count=100,
        #                                  filter='all')['items']
        #
        # for post_id in checking_posts:
        #     self.owner_id_list.append(post_id['owner_id'])
        #     self.id_list.append(post_id['id'])
        #     # count_str += 1
        #     # print(f"{count_str} - {post_id}")
        #
        # time.sleep(0.3)

        self.dict_posts = dict(
            zip(self.id_list, self.owner_id_list))  # Записываем ID в словарь для дальнейшей работы с ним.

        for key, value in self.dict_posts.items():
            """Усыпляем каждый раз потому что того требует VkAPI."""
            time.sleep(0.3)

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

        self.final_dict = dict(Counter(self.favorite_users_dict).most_common(50))  # Выводим 50 активных пользователей.

        return self.final_dict


def main():
    start_search = SearchForActive('uvdgrodno')
    print(start_search.check_posts())
    # print("---%s second ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
