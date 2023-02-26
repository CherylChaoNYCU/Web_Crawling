import json

with open('all_article.jsonl','r') as f:
    data = json.load(f)
print(len(data))

# for i in range(20):
#     print(data[i])
#     if(data[i]['date: '] == '0101'):
#         print(data[i]['date: '])
# dict = {'gtoamdk7': 2, 'Swando': 1, 'ninimikoo': 1, 'Kelite': 1, 'w2884939': 1, 'Vek1112': 1, 'Eligor41': 1, 'ptt821105': 1, 'SCurry30': 1, 'diminifish': 1}
# items = dict.items()
# keys = []
# values = []
# for item in items:
#     keys.append(item[0]), values.append(item[1])
# print(keys[0])
# print(values)

a = '0203'
b = '0511'

print(int(a) - int(b))