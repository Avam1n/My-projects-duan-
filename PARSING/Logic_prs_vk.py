import re
import vk
from vk_prs import ParsVk
from tkinter import *

session = vk.Session('9451b8e79451b8e79451b8e732942d3cd9994519451b8e7f627814adc6248d278f52c5f')
vk_api = vk.API(session, v="5.131")


class ParsVk:
    url = ''
    list_users = []

    def __init__(self, url):
        self.url = url

    def req_url(self):
        try:
            req = re.search(r'((?P<id1>-?\d+)_(?P<id2>\d+))', self.url)
            own_id = int(req['id1'])
            it_id = int(req['id2'])
            check_list = vk_api.likes.getList(type='post', owner_id=own_id, item_id=it_id,
                                              extended=1, count=1000)
            self.list_users = vk_api.users.get(user_ids=[i['id'] for i in check_list['items']], fields='city')
            return check_list
        except TypeError as err:
            return f'Что то пошло не так... видимо ссылка не из ВК!'

    @property
    def create_a_all_list(self):
        try:
            keys = {'id', 'first_name', 'last_name', 'can_access_closed',
                    'is_closed', 'type'}
            a = ParsVk.req_url(self)
            my_list = a['items']
            close_list = list(filter(lambda d: d.keys() == keys, my_list))
            list_users = []
            for i in close_list:
                if i['is_closed'] != True:
                    list_users.append(i)
            return ["||ID: {:^10}||Name: {:<15}||Last_name: {:<20}||Link: https://vk.com/id{}".format(
                elem['id'], elem['first_name'],
                elem['last_name'], elem['id'],
                end='\n') for elem in list_users]
        except TypeError as Tyerr:
            print(Tyerr)

    @property
    def create_a_open_list(self):
        keys_with_city = {'id', 'first_name', 'last_name', 'can_access_closed',
                          'is_closed', 'city'}
        a = ParsVk.req_url(self)
        open_list = list(filter(lambda d: d.keys() == keys_with_city, self.list_users))
        list_users = []
        for i in open_list:
            if i['is_closed'] != True:
                list_users.append(i)

        for elem in list_users:
            spk = elem['city']
            print("||ID: {:^10}||Name: {:<15}||Last_name: {:<20}||City: {:<20}||Link: https://vk.com/id{}".format(
                elem['id'], elem['first_name'],
                elem['last_name'], spk['title'], elem['id'],
                end='\n'))

        return list_users


window = Tk()
window.title("Парсинг VK")

all_list = StringVar()
all_with_city_list = StringVar()

w = window.winfo_screenwidth()
h = window.winfo_screenheight()
w = w // 2  # середина экрана
h = h // 2
w = w - 200  # смещение от середины
h = h - 200
window.geometry('1000x650+450+200'.format(w, h))

url_lbl = Label(window, text='Тут URL поста -->')
url_lbl.grid(column=0, row=1)

url_entr = Entry(window, width=100, textvariable=all_list)
url_entr.grid(column=1, row=1)

bttn = Button(window, text='Парсим!', command=ParsVk.create_a_all_list)
bttn.grid(column=2, row=1)

url_out = Label(window)
url_out.grid(column=1, row=3)

window.mainloop()

if __name__ == '__main__':
    prs = ParsVk(url_entr.get())
    # print(f'Данный после урла --->{prs.req_url()}')
    # print('*' * 80)
    print(f'Данный закрытый лист --->{prs.create_a_all_list}')
    # print('*' * 80)
    print(f'Данный открытый лист --->{prs.create_a_open_list}')
    # print('*' * 80)
    # prs.create_a_open_list
    window = Tk()
    window.title("Парсинг VK")

    all_list = StringVar()
    all_with_city_list = StringVar()

    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 200  # смещение от середины
    h = h - 200
    window.geometry('1000x650+450+200'.format(w, h))
