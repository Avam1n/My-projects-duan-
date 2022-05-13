import re
from urllib.parse import urlparse
import vk

session = vk.Session('9451b8e79451b8e79451b8e732942d3cd9994519451b8e7f627814adc6248d278f52c5f')
vk_api = vk.API(session, v="5.131")


class ParsVk:

    def __init__(self, url):
        self.url = urlparse(url)

    def req_url(self):
        req = re.search(r'((?P<id1>-?\d+)_(?P<id2>\d+))', self.url.query)
        own_id = req['id1']
        it_id = req['id2']
        inna = vk_api.likes.getList(type="post", owner_id=own_id, item_id=it_id, extended=1)
        return inna

    @property
    def create_a_close_list(self):
        a = ParsVk.req_url(self)
        close_list = []
        for i in a['items']:
            b = i['is_closed']
            if b == True:
                close_list.append(i)
        return close_list

    @property
    def create_a_open_list(self):
        a = ParsVk.req_url(self)
        open_list = []
        for i in a['items']:
            b = i['is_closed']
            if b == False:
                open_list.append(i)
        return open_list


if __name__ == '__main__':
    prs = ParsVk('https://vk.com/academyofman?w=wall-45595714_10452971')
    prs.req_url()
    print('*' * 80)
    print(prs.create_a_close_list)
    print('*' * 80)
    print(prs.create_a_open_list)
    print('*' * 80)

    for i in prs.create_a_close_list:
        print(i)

    print('*' * 80)

    for i in prs.create_a_open_list:
        print(i)
