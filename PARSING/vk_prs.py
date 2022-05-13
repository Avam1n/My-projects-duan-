import re


class ParsVk:

    def __init__(self, url):
        self.url = url

    def req_url(self):
        req = re.findall(r'(((?<=wall)|(?<=photo))-?(?P<id1>\d+)_(?P<id2>\d+))', self.url)
        return req

    def pars_id(self):
        list_id = []
        for i in self.req_url():
            if len(i) > 1:
                list_id.append(i)
        return list_id


if __name__ == '__main__':
    prs = ParsVk('https://vk.com/fin4es?z=photo378516444_457241942%2Fphotos378516444')
    print(prs.req_url())
    print('*' * 80)
    print(prs.pars_id())
    print('*' * 80)
    prs.show_info()
