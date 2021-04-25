import ast
import inspect
import dis
import os
import types

globals_opcodes = [dis.opmap['LOAD_GLOBAL'], dis.opmap['DELETE_GLOBAL'], dis.opmap['STORE_GLOBAL']]


def obj_to_dict(obj):
    fields = {'attrs': {f: obj.__getattribute__(f) for f in dir(obj) if
                        not callable(getattr(obj, f)) and not (f.startswith(('__', '_')))},
              'type': 'class object' if inspect.isclass(obj.__class__) else 'func object',
              'name': obj.__class__.__name__}
    try:
        fields["code"] = inspect.getsource(obj.__class__)
    except IOError:
        print('Getsource error!')
        return None
    if inspect.isfunction(obj.__class__):
        fields['globals'] = {}
        for instr in dis.get_instructions(obj):
            if instr.opcode in globals_opcodes:
                fields['globals'][instr.argval] = obj.__globals__[instr.argval]
    return fields


def class_to_dict(obj):
    fields = {'type': 'function' if inspect.isfunction(obj) else 'class', 'name': obj.__name__}
    try:
        fields['code'] = get_short_lambda_source(obj) \
            if isinstance(obj, types.LambdaType) and obj.__name__ == "<lambda>"\
            else inspect.getsource(obj)
    except IOError:
        print('Get source error!')
        return None
    if inspect.isfunction(obj):
        fields['globals'] = {}
        for instr in dis.get_instructions(obj):
            if instr.opcode in globals_opcodes:
                if instr.argval != 'print':
                    fields['globals'][instr.argval] = obj.__globals__[instr.argval]
    return fields


def get_object(object_dict: dict):
    namespace = {} if object_dict.get('globals') is None else object_dict.get('globals')
    exec(object_dict.get('code'), namespace)
    if object_dict.get('type') in ['function', 'class', 'func object']:
        if object_dict.get('name') == '<lambda>':
            return eval(object_dict.get('code'), namespace)
        return namespace.get(object_dict.get('name'))
    elif object_dict.get('type') == 'class object':
        class_obj = namespace.get(object_dict.get('name'))
        params = {arg: object_dict.get('attrs')[arg]
                  for arg in inspect.getfullargspec(class_obj.__init__)[0][1:]}
        return namespace.get(object_dict.get('name'))(**params)
    return object_dict


def get_object_recursive(obj: dict):
    if obj.get('type') is not None:
        return get_object(obj)
    for key, value in obj.items():
        if isinstance(value, dict):
            if value.get('type') is not None:
                obj[key] = get_object(value)
            else:
                get_object_recursive(value)
        elif isinstance(value, (tuple, list)):
            for i, enum in enumerate(value):
                if isinstance(enum, dict):
                    value[i] = get_object_recursive(enum)
    return obj


def get_short_lambda_source(lambda_func):
    """Return the source of a (short) lambda function.
    If it's impossible to obtain, returns None.
    """
    try:
        source_lines, _ = inspect.getsourcelines(lambda_func)
    except (IOError, TypeError):
        return None

    if len(source_lines) != 1:
        return None

    source_text = os.linesep.join(source_lines).strip()

    source_ast = ast.parse(source_text)
    lambda_node = next((node for node in ast.walk(source_ast)
                        if isinstance(node, ast.Lambda)), None)
    if lambda_node is None:
        return None

    lambda_text = source_text[lambda_node.col_offset:]
    lambda_body_text = source_text[lambda_node.body.col_offset:]
    min_length = len('lambda:_')
    while len(lambda_text) > min_length:
        try:
            code = compile(lambda_body_text, '<unused filename>', 'eval')

            if len(code.co_code) == len(lambda_func.__code__.co_code):
                return lambda_text
        except SyntaxError:
            pass
        lambda_text = lambda_text[:-1]
        lambda_body_text = lambda_body_text[:-1]
    return None
