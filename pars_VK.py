import vk
import config
from Super_bot import prs

session = vk.Session(config.Token_VK)
vk_api = vk.API(session, v="5.131")
# print(vk_api.users.get(user_id=378516444))
# print(vk_api.likes.getList(type="post", owner_id=121124562, item_id=4094))
inna = vk_api.likes.getList(type="post", owner_id=-18923125, item_id=1355011, extended=1)
print(inna)
print('*' * 88)

with open('search_vk_post', 'w', encoding='utf-8') as file:
    for i in inna['items']:
        file.write(str(inna['count']) + '\n' + '\n' + str(i) + '\n' + '\n')
        file.write('{0},'.format(str(inna["count"])), )

if __name__ == '__main__':
    pass
