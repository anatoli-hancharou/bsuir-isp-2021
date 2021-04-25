from modules.JsonSerializerCreator import JsonSerializerCreator
from modules.SerializerCreator import Creator


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.gender = "female"

    def set_name(self, name):
        self.name = name


a = 3
b = 4
c = 5


def hello(name):
    print(f"hello, {name} _ {c}!")


def create_serializer(creator: Creator):
    return creator.create_serializer()


def _main():
    serializer = create_serializer(JsonSerializerCreator())
    person = Person("Alex", 32)
    # obj = serializer.loads(func_dict)
    test = {'name': 'Sarah', 'age': 11}
    lam = lambda x: b*x

    person_dict = serializer.dumps(person)
    print(person_dict)
    #person_class = serializer.loads(person_dict)
    #print(person_class)

    # person = person_class('Alex', 13)
    # person.set_name('Antony')
    # print(person.name)


if __name__ == "__main__":
    _main()