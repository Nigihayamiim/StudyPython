person = {'name': '欧阳娜娜', 'sex': '女', 'age': 20}
for p in person:
    print(person.get(p,'这是默认值啊'))

person_keys = person.keys()
person_value = person.values()
person_item = person.items()
print(person_keys, '\n', person_value, '\n', person_item)
for item in person_item:
    print('key:', item[0], 'value:', item[1])


