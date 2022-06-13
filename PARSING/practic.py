from tkinter import *
import re
import vk


def req_url():
    try:
        req = re.search(r'((?P<id1>-?\d+)_(?P<id2>\d+))', url_entr.get())
        own_id = int(req['id1'])
        it_id = int(req['id2'])
        check_list = vk_api.likes.getList(type='post', owner_id=own_id, item_id=it_id,
                                          extended=1, count=1000)
        list_users = vk_api.users.get(user_ids=[i['id'] for i in check_list['items']], fields='city')
        return check_list
    except TypeError as err:
        url_out.insert(1.0, f'Что то пошло не так... видимо ссылка не из ВК!')


def create_a_open_list():
    keys_with_city = {'id', 'first_name', 'last_name', 'can_access_closed',
                      'is_closed', 'city'}
    a = req_url()
    list_users_with_city = vk_api.users.get(user_ids=[i['id'] for i in a['items']], fields='city')
    open_list = list(filter(lambda d: d.keys() == keys_with_city, list_users_with_city))
    list_users = []
    for i in open_list:
        if i['is_closed'] != True:
            list_users.append(i)

    print(list_users[1])
    for elem in list_users:
        spk = elem['city']
        url_out.insert(1.0,
                       "ID: {:^10}||Name: {:<15}Last_name: {:<20}City: {:<20}Link: https://vk.com/id{}\n".format(
                           elem['id'], elem['first_name'],
                           elem['last_name'], spk['title'], elem['id']))


session = vk.Session('9451b8e79451b8e79451b8e732942d3cd9994519451b8e7f627814adc6248d278f52c5f')
vk_api = vk.API(session, v="5.131")
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

url_lbl = Label(window, text='Введите URL поста:')
url_lbl.grid(column=1, row=1)

url_entr = Entry(window, width=100, textvariable=all_list)
url_entr.grid(column=1, row=2)

bttn = Button(window, text='Парсим!', command=create_a_open_list)
bttn.grid(column=2, row=2)

url_lbl = Label(window, text='Окно вывода:')
url_lbl.grid(column=1, row=3)

url_out = Text(window, width=130, height=22, bg="black", fg="white", wrap=WORD)
url_out.grid(column=1, row=4)

# scrolly = Scrollbar()
# scrolly.grid(column=2, row=4, ipady=150)
#
# url_out.config(yscrollcommand=scrolly.set)

window.mainloop()
