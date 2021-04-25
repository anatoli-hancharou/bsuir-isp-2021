import unittest
import sys
from modules.JsonSerializerCreator import JsonSerializerCreator
from modules.PickleSerializerCreator import PickleSerializerCreator
from modules.YamlSerializaerCreator import YamlSerializerCreator
from modules.TomlSerializerCreator import TomlSerializerCreator
from modules.JsonSerialization import from_json, _json_to_dict, _json_to_list, _json_to_basic


def hello(name):
    print(f"hello, {name}!")


abc = 'World'


def hello_world(greeting):
    return f"{greeting}, {abc}!"


class TestDump(unittest.TestCase):
    def setUp(self):
        self.serializers = [JsonSerializerCreator(), YamlSerializerCreator(),
                            TomlSerializerCreator(), PickleSerializerCreator()]

    def test_dict_dumps(self):
        self.results = ["{'name':'Sarah', 'age':12}", 'age: 12\nname: Sarah\n',
                        'name = "Sarah"\nage = 12\n', '(dp0\nVname\np1\nVSarah\np2\nsVage\np3\nI12\ns.']

        for item in zip(self.serializers, self.results):
            serializer = item[0].create_serializer()
            with self.subTest(case=serializer):
                self.assertEqual(serializer.dumps({'name': 'Sarah', 'age': 12}), item[1])

    def test_func_dumps(self):
        self.results = [
            """{'type':'function', 'name':'hello', 'code':'def hello(name):\n    print(f"hello, {name}!")\n\', \'globals\':{}}""",
            """code: "def hello(name):\\n    print(f\\"hello, {name}!\\")\\n"\nglobals: {}\nname: hello\ntype: function\n""",
            'type = "function"\nname = "hello"\ncode = "def hello(name):\\n    print(f\\"hello, {name}!\\")\\n"\n\n[globals]\n',
            '(dp0\nVtype\np1\nVfunction\np2\nsVname\np3\nVhello\np4\nsVcode\np5\nVdef hello(name):\\u000a    print(f"hello, {name}!")\\u000a\np6\nsVglobals\np7\n(dp8\ns.']

        for item in zip(self.serializers, self.results):
            serializer = item[0].create_serializer()
            with self.subTest(case=serializer):
                self.assertEqual(serializer.dumps(hello), item[1])


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.serializers = [JsonSerializerCreator(), YamlSerializerCreator(),
                            TomlSerializerCreator(), PickleSerializerCreator()]

    def test_lambda_loads(self):
        for item in self.serializers:
            serializer = item.create_serializer()
            with self.subTest(case=serializer):
                _lambda = lambda x: x * x
                lambda_dict = serializer.dumps(_lambda)
                self.assertEqual(serializer.loads(lambda_dict)(5), _lambda(5))

    def test_dict_loads(self):
        for item in self.serializers:
            serializer = item.create_serializer()
            with self.subTest(case=serializer):
                test_dict = {'name': 'Sarah', 'age': 12}
                dct = serializer.dumps(test_dict)
                result = serializer.loads(dct)
                self.assertDictEqual(result, test_dict)

    def test_func_loads(self):
        for item in self.serializers:
            serializer = item.create_serializer()
            with self.subTest(case=serializer):
                func_dict = serializer.dumps(hello_world)
                self.assertEqual(serializer.loads(func_dict)('Hello'), 'Hello, World!')

    def test_load(self):
        for item in self.serializers:
            serializer = item.create_serializer()
            with self.subTest(case=serializer):
                func_dict = serializer.dumps(hello_world)
                self.assertEqual(None, serializer.load('~!!@#.'))


class TestCustomJsonSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer = JsonSerializerCreator()
        self.test_cases_from_json = ["    {'name':'Sarah', 'age':11}", "('name':'Sarah', 'age':11}",
                                     "!{'name':'Sarah', 'age':11}", "trash{'name':'Sarah', 'age':11}"]
        self.test_cases_to_dist = ["{'name':'Sarah', 'age':11", "('name:'Sarah', 'age':11}"]

    def test_from_json_throws_ex(self):
        for case in self.test_cases_from_json:
            with self.subTest(case=case):
                self.assertRaises(IOError, lambda: from_json(case))

    def test_to_dict_returns_none(self):
        for case in self.test_cases_to_dist:
            with self.subTest(case=case):
                self.assertEqual(None, _json_to_dict(case, 0))

    def test_to_dict_throws_ex(self):
        for case in self.test_cases_to_dist:
            with self.subTest(case=case):
                self.assertRaises(IOError, lambda: _json_to_dict(case, 100))

    def test_to_list_throws_ex(self):
        for case in self.test_cases_to_dist:
            with self.subTest(case=case):
                self.assertRaises(IOError, lambda: _json_to_list(case, 100))

    def test_to_basic_throws_ex(self):
        for case in self.test_cases_to_dist:
            with self.subTest(case=case):
                self.assertRaises(IOError, lambda: _json_to_basic(case, 100))




def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDump('test_dict_dumps'))
    suite.addTest(TestDump('test_func_dumps'))
    suite.addTest(TestLoad('test_dict_loads'))
    suite.addTest(TestLoad('test_lambda_loads'))
    suite.addTest(TestLoad('test_func_loads'))
    suite.addTest(TestLoad('test_load'))
    suite.addTest(TestCustomJsonSerializer('test_from_json_throws_ex'))
    suite.addTest(TestCustomJsonSerializer('test_to_dict_returns_none'))
    suite.addTest(TestCustomJsonSerializer('test_to_dict_throws_ex'))
    suite.addTest(TestCustomJsonSerializer('test_to_basic_throws_ex'))
    return suite


def run_tests():
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    runner.run(test_suite())
