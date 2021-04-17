from Serializers.Serializer import Serializer
from SerializationTools import tools
import inspect


class JsonSerializer(Serializer):
    def dump(self, obj, fp: str):
        json_str = to_json(obj)
        try:
            with open(fp, 'w') as f:
                f.write(json_str)
        except IOError:
            print('An IOError has occurred!')
        return json_str

    def dumps(self, obj):
        return to_json(obj)

    def load(self, fp):
        try:
            with open(fp, 'r') as f:
                script = f.read()
        except IOError:
            print(f'An IOError has occurred: failed to open {fp}')
            return None
        return from_json(script)

    def loads(self, s):
        return from_json(s)


def to_json(obj):
    if isinstance(obj, (list, tuple)):
        return _tuple_or_list_to_json(obj)
    elif isinstance(obj, dict):
        return _dict_to_json(obj)
    elif inspect.isclass(obj) or inspect.isfunction(obj):
        return _dict_to_json(tools.class_to_dict(obj))
    else:
        return _dict_to_json(tools.obj_to_dict(obj))


def _tuple_or_list_to_json(obj):
    temp_list = []
    for i in obj:
        if isinstance(i, (int, float, str, bool, type(None))):
            temp_list.append(_basic_type_to_json(i))
        elif isinstance(i, (list, tuple)):
            temp_list.append(_tuple_or_list_to_json(i))
        elif isinstance(i, dict):
            temp_list.append(_dict_to_json(i))
        elif inspect.isclass(obj) or inspect.isfunction(obj):
            temp_list.append(_dict_to_json(tools.class_to_dict(i)))
        else:
            temp_list.append(_dict_to_json(tools.obj_to_dict(i)))
    output_str = ', '.join(temp_list)
    return '[ ' + output_str + ' ]'


def _basic_type_to_json(obj):
    if isinstance(obj, str):
        return f"'{obj}'"
    elif isinstance(obj, type(None)):
        return "none"
    elif isinstance(obj, bool):
        return "true" if obj else "false"
    elif isinstance(obj, (int, float)):
        return f"{obj}"


def _dict_to_json(dct):
    temp_list = []
    for key, value in dct.items():
        if isinstance(value, (int, float, str, bool, type(None))):
            temp_list.append(_json_element(key, _basic_type_to_json(value)))
        elif isinstance(value, (list, tuple)):
            temp_list.append(_json_element(key, _tuple_or_list_to_json(value)))
        elif isinstance(value, dict):
            temp_list.append(_json_element(key, _dict_to_json(value)))
        elif inspect.isclass(value) or inspect.isfunction(value):
            temp_list.append(_json_element(key, _dict_to_json(tools.class_to_dict(value))))
        else:
            temp_list.append(_json_element(key, _dict_to_json(tools.obj_to_dict(value))))

    output_str = ', '.join(temp_list)
    return f'{{{output_str}}}'


def _json_element(k, v):
    return f"'{k}':{v}"


def from_json(text=' '):
    if text[0] == '{':
        object_dict = _json_to_dict(text, 0)[0]
        if object_dict.get('type') is None:
            return tools.get_object_recursive(object_dict)
        else:
            return tools.get_object(object_dict)
    elif text[0] == '[':
        return _json_to_list(text, 1)[0]
    else:
        raise IOError('Json file should start with symbols: "{" or "["')


def _json_to_list(text, start):
    output = []
    i = start
    while i < len(text) - 1:
        i += 1
        if text[i] == ']':
            return output, i
        if text[i] == ' ' or text[i] == ',':
            continue
        if text[i] == '[':
            elem = _json_to_list(text, i + 1)
            output.append(elem[0])
            i = elem[1]

        elif text[i] == '{':
            elem = _json_to_dict(text, i + 1)
            output.append(elem[0])
            i = elem[1]
        else:
            elem = _json_to_basic(text, i)
            output.append(elem[0])
            i = elem[1]
    raise IOError("Неверный формат")


def _json_to_dict(text, start):
    output = {}
    i = start
    while i < len(text) - 1:
        i += 1
        if text[i] == '}':
            return output, i
        try:
            elem = _get_token(text, i)
            elem2 = _get_token(text, elem[1] + 1)
            output[elem[0]] = elem2[0]
            i = elem2[1]
        except IOError as error:
            return None
    raise IOError("Неверный формат")


def _json_to_basic(text, start):
    tokens = []
    quot = False
    is_float = False
    for i in range(start, len(text)):
        if (text[i] in ': ') and not quot:
            continue
        if text[i] in ',]}' and not quot:
            def to_int_or_float(s, f):
                try:
                    if f:
                        return float(s)
                    return int(s)
                except ValueError:
                    return None

            switcher = {'true': True, 'false': False, 'none': None}
            str = ''.join(tokens)
            return switcher.get(str, to_int_or_float(str, is_float)), i - 1
        if text[i] == "'" and quot:
            return ''.join(tokens), i
        if text[i] == "'":
            quot = not quot
            continue
        if text[i] == '.':
            is_float = True
        tokens.append(text[i])
    raise IOError("Неверный формат")


def _get_token(text, start):
    for i in range(start, len(text)):
        if text[i] in ', :':
            continue
        if text[i] in '}]':
            raise IOError(f"{i}")
        if text[i] == '[':
            return _json_to_list(text, i + 1)
        elif text[i] == '{':
            return _json_to_dict(text, i)
        else:
            return _json_to_basic(text, i)
