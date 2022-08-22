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

    def __init__(self, group_id):
        self.group_id = group_id

    def check_group(self):
        """Принимаем и настраиваем на вывод id группы (пример: ввод -->'cybersportby', вывод --> '-78017410')."""
        try:
            match self.group_id:
                case int(self.group_id):
                    get_group = self.group_id
                    return get_group
                case _:
                    get_group = vk_api.groups.getById(group_id=self.group_id)
                    get_group_id = get_group[0]
                    group_id = get_group_id.get('id')
                    return f'-{group_id}'
        except Exception as err:
            return f'Что-то пошло не так, описание ошибки ---> {err}'

    def check_posts(self, get_offset: int) -> dict:
        """Данный метод нужен для того, чтобы перебрать и взять нужную информацию по ВСЕМ постам группы, и определяем
        самого активного участника.(определение проходит исключительно по лайкам)"""

        offset = 0
        count = 0

        while True:
            checking_posts = vk_api.wall.get(owner_id=SearchForActive.check_group(self),
                                             offset=offset,
                                             count=100,
                                             filter='all')['items']
            # for post_id in checking_posts:
            #     self.owner_id_list.append(post_id['owner_id'])
            #     self.id_list.append(post_id['id'])
            #     count += 1
            #     print(f"{count} - {post_id}")
            # offset += 100
            # time.sleep(0.4)
            # count += 1
            # if offset == get_offset:
            #     break
            time.sleep(0.4)
            if offset == get_offset:
                break
            elif len(checking_posts) != 0:
                for post_id in checking_posts:
                    self.owner_id_list.append(post_id['owner_id'])
                    self.id_list.append(post_id['id'])
                    count += 1
                    print(f"{count} - {post_id}")
                offset += 100
                count += 1
            else:
                # if offset == get_offset:
                #     break
                break
        self.dict_posts = dict(
            zip(self.id_list, self.owner_id_list))  # Записываем ID в словарь для дальнейшей работы с ним.

        for key, value in self.dict_posts.items():
            """Усыпляем каждый раз потому что того требует VkAPI."""

            offset_likes = 0
            count = 1
            while True:
                time.sleep(0.6)
                check_list = vk_api.likes.getList(type='post',
                                                  owner_id=value,
                                                  item_id=key,
                                                  extended=0,
                                                  count=1000,
                                                  offset=offset_likes)

                checking_item_list = check_list['items']
                for element in checking_item_list:
                    self.favorite_users.append(element)
                    print(f'{count}---{element}')
                    count += 1

                offset_likes += 1000

                # if len(check_list['items']) != 0:
                #     for element in check_list['items']:
                #         print(f'{count}---{element}')
                #         self.favorite_users.append(element)
                #         count += 1
                if len(checking_item_list) == 0:
                    break

        for element in self.favorite_users:
            self.favorite_users_dict[element] = self.favorite_users_dict.get(element,
                                                                             0) + 1  # Добавляем колличество раз встречаемых ID.

        self.final_dict = dict(Counter(self.favorite_users_dict).most_common(50))  # Выводим 50 активных пользователей.

        return self.final_dict

    def open_account_check(self):
        try:
            open_account_list = vk_api.users.get(user_ids=[k for k, v in self.final_dict.items()],
                                                 fields='city')
            list_active_users = []
            for i in open_account_list:  # В цикле поэлементно проверяем на соответствие желаемому условию.
                if i.get('is_closed') is not True and i.get('deactivated') != 'deleted':
                    list_active_users.append(i)
            for key, value in self.final_dict.items():
                for item in list_active_users:
                    if key == item.get('id'):
                        a = dict(like=f'{value}')
                        item.update(a)
            return list_active_users
        except Exception as err:
            print(f'{err}-- open_account_check')
            return f'Oops!\nЧто-то пошло не так... в создании списка.'

    def show_file(self):  # Реализуем показ нужной нам информации.
        try:
            list_users = SearchForActive.open_account_check(self)
            with open(r'Active_users.html', 'w', encoding='UTF-8') as file:
                count = 1
                for element in list_users:
                    element_with_city_item = element.get('city', f'{"-------"}')
                    print(
                        f"-{count}-"
                        f"||ID: {element.get('id'):<10} "
                        f"||Name: {element.get('first_name'):<15} "
                        f"||Last_name: {element.get('last_name'):<20} "
                        f"||City: --{element_with_city_item['title'] if element_with_city_item is not str(element_with_city_item) else element_with_city_item:<18} "
                        f"||Liked posts: {element.get('like'):<5}"
                        f"||Link:   <a href='https://vk.com/id{element.get('id')}'>https://vk.com/id{element.get('id')}</a>" + "<br>",
                        file=file)  # Настроили то как будет выглядеть информация в файле.
                    count += 1
            return file
        except Exception as err:
            if file is None:
                return f'Oops!\nЧто-то пошло не так... в отображении.'
            else:
                print(err)
                return f'Oops!\nЧто-то пошло не так... в отображении.'


def main(some, offset):
    start_search = SearchForActive(some)
    start_search.check_posts(offset)
    start_search.open_account_check()
    start_search.show_file()
    return f'{"Выполнено за --- %.0f --- секунд(ы)! :)" % (time.time() - start_time)}'


if __name__ == '__main__':
    main('zloyshkolnik', 100)
