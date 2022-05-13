import vk
import config
from PARSING.vk_prs import ParsVk

session = vk.Session(config.Token_VK)
vk_api = vk.API(session, v="5.131")


class DataPars(ParsVk):

    def get_data(self):
        inna = vk_api.likes.getList(type="post", owner_id=own_id, item_id=it_id, extended=1)
        return inna


# with open('search_vk_post', 'w', encoding='utf-8') as file:
#     for i in inna['items']:
#         file.write(str(inna['count']) + '\n' + '\n' + str(i) + '\n' + '\n')
#         file.write('{0},'.format(str(inna["count"])), )

if __name__ == '__main__':
    dp = DataPars('https://vk.com/fin4es?z=photo378516444_457241942%2Fphotos378516444')
    print(dp.get_data())
