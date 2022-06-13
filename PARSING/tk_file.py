from tkinter import *
import vk_prs
from vk_prs import ParsVk


def show_pars():
    prs = ParsVk(url_entr)
    url_out.configure(prs.create_a_close_list)


window = Tk()
window.title("Парсинг VK")

w = window.winfo_screenwidth()
h = window.winfo_screenheight()
w = w // 2  # середина экрана
h = h // 2
w = w - 200  # смещение от середины
h = h - 200
window.geometry('1000x650+450+200'.format(w, h))

token_lbl = Label(window, text='Тут Ваш токен -->')
token_lbl.grid(column=0, row=0)

token_entr = Entry(window, width=100)
token_entr.grid(column=1, row=0)

url_lbl = Label(window, text='Тут URL поста -->')
url_lbl.grid(column=0, row=1)

url_entr = Entry(window, width=100)
url_entr.grid(column=1, row=1)

bttn = Button(window, text='Парсим!', command=show_pars)
bttn.grid(column=2, row=1)

url_out = Label(window, text='')
url_out.grid(column=1, row=3)

window.mainloop()
