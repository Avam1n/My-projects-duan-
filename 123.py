import re
from urllib.parse import urlparse

url = 'https://vk.com/academyofman?w=wall-45595714_10452971'
url2 = 'https://vk.com/academyofman?w=wall-45595714_10452971&z=photo-45595714_457550107%2Fwall-45595714_10452971'
url3 = 'https://vk.com/id319591233?w=wall319591233_252'
url4 = 'https://vk.com/id319591233?z=photo319591233_456239726%2Falbum319591233_00%2Frev'
#
#
# print(req)


a = urlparse(url3)
req = re.search(r'((?P<id1>-?\d+)_(?P<id2>\d+))', a.query)
b = req['id1']
c = req['id2']
# print(a)
# print('*' * 88)
print(b)
print(c)
# print('*' * 88)
# print(a.query)
# print('*' * 88)
# print(a.query)
