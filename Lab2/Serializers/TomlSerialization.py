import toml
from Serializers.Serializer import Serializer
from SerializationTools import tools
import inspect


class TomlSerializer(Serializer):
    def dump(self, obj, fp: str):
        toml_str = CustomTomlSerializer.dumps(obj)
        try:
            with open(fp, 'w') as f:
                f.write(toml_str)
        except IOError:
            print("An IOError has occurred!")
        return toml_str

    def dumps(self, obj):
        return CustomTomlSerializer.dumps(obj)

    def load(self, fp):
        try:
            with open(fp, 'r') as f:
                script = f.read()
        except IOError:
            print(f"An IOError has occurred: failed to open {fp}")
            return
        return CustomTomlSerializer.loads(script)

    def loads(self, s):
        return CustomTomlSerializer.loads(s)


class CustomTomlSerializer:
    @staticmethod
    def dumps(obj):
        if isinstance(obj, (list, tuple)):
            return _tuple_or_list_to_toml(obj)
        elif isinstance(obj, dict):
            return toml.dumps(_dict_to_toml(obj))
        elif inspect.isclass(obj) or inspect.isfunction(obj):
            return toml.dumps(_dict_to_toml(tools.class_to_dict(obj)))
        else:
            return toml.dumps(_dict_to_toml(tools.obj_to_dict(obj)))

    @staticmethod
    def loads(s: str):
        object_dict = {}
        try:
            object_dict = toml.loads(s)
        except Exception as exc:
            print(exc)
        if object_dict.get('type') is None:
            return tools.get_object_recursive(object_dict)
        else:
            return tools.get_object(object_dict)


def _dict_to_toml(dct):
    temp_dct = {}
    for key, value in dct.items():
        if isinstance(value, (int, float, str, bool, type(None))):
            temp_dct[key] = value
        elif isinstance(value, (list, tuple)):
            temp_dct[key] = _tuple_or_list_to_toml(value)
        elif isinstance(value, dict):
            temp_dct[key] = _dict_to_toml(value)
        elif inspect.isclass(value) or inspect.isfunction(value):
            temp_dct[key] = _dict_to_toml(tools.class_to_dict(value))
        else:
            temp_dct[key] = _dict_to_toml(tools.obj_to_dict(value))
    return temp_dct


def _tuple_or_list_to_toml(obj):
    temp_list = []
    for i in obj:
        if isinstance(i, (int, float, str, bool, type(None))):
            temp_list.append(i)
        elif isinstance(i, (list, tuple)):
            temp_list.append(_tuple_or_list_to_toml(i))
        elif isinstance(i, dict):
            temp_list.append(_dict_to_toml(i))
        elif inspect.isclass(i) or inspect.isfunction(i):
            temp_list.append(_dict_to_toml(tools.class_to_dict(i)))
        else:
            temp_list.append(_dict_to_toml(tools.obj_to_dict(i)))
    return temp_list

