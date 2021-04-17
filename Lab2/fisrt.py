from Creators.JsonSerializerCreator import JsonSerializerCreator

text = "Hello"


def func():
    print(text)


serializer = JsonSerializerCreator().create_serializer()
serializer.dump(func, 'file.json')

