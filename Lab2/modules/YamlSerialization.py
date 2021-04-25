import yaml
from modules.Serializer import Serializer
import inspect
from modules import tools


class YamlSerializer(Serializer):
    def dump(self, obj, fp: str):
        yaml_str = CustomYamlSerializer.dumps(obj)
        try:
            with open(fp, 'w') as f:
                f.write(yaml_str)
        except IOError:
            print("An IOError has occurred!")
        return yaml_str

    def dumps(self, obj):
        return CustomYamlSerializer.dumps(obj)

    def load(self, fp):
        try:
            with open(fp, 'r') as f:
                script = f.read()
        except IOError:
            print(f"An IOError has occurred: failed to open {fp}")
            return
        return CustomYamlSerializer.loads(script)

    def loads(self, s):
        return CustomYamlSerializer.loads(s)

    def get_dict(self, text):
        return yaml.safe_load(text)


class CustomYamlSerializer:
    @staticmethod
    def dumps(obj):
        if isinstance(obj, (list, tuple)):
            return _tuple_or_list_to_yaml(obj)
        elif isinstance(obj, dict):
            return yaml.dump(_dict_to_yaml(obj))
        elif inspect.isclass(obj) or inspect.isfunction(obj):
            return yaml.dump(_dict_to_yaml(tools.class_to_dict(obj)))
        else:
            return yaml.dump(_dict_to_yaml(tools.obj_to_dict(obj)))

    @staticmethod
    def loads(s: str):
        object_dict = {}
        try:
            object_dict = yaml.safe_load(s)
        except yaml.YAMLError as exc:
            print(exc)
        if object_dict.get('type') is None:
            return tools.get_object_recursive(object_dict)
        else:
            return tools.get_object(object_dict)


def _dict_to_yaml(dct):
    temp_dct = {}
    for key, value in dct.items():
        if isinstance(value, (int, float, str, bool, type(None))):
            temp_dct[key] = value
        elif isinstance(value, (list, tuple)):
            temp_dct[key] = _tuple_or_list_to_yaml(value)
        elif isinstance(value, dict):
            temp_dct[key] = _dict_to_yaml(value)
        elif inspect.isclass(value) or inspect.isfunction(value):
            temp_dct[key] = _dict_to_yaml(tools.class_to_dict(value))
        else:
            temp_dct[key] = _dict_to_yaml(tools.obj_to_dict(value))
    return temp_dct


def _tuple_or_list_to_yaml(obj):
    temp_list = []
    for i in obj:
        if isinstance(i, (int, float, str, bool, type(None))):
            temp_list.append(i)
        elif isinstance(i, (list, tuple)):
            temp_list.append(_tuple_or_list_to_yaml(i))
        elif isinstance(i, dict):
            temp_list.append(_dict_to_yaml(i))
        elif inspect.isclass(i) or inspect.isfunction(i):
            temp_list.append(_dict_to_yaml(tools.class_to_dict(i)))
        else:
            temp_list.append(_dict_to_yaml(tools.obj_to_dict(i)))
    return temp_list

