"""
系统参数
"""


def get_environ(key, default_value=None):
    """获取环境变量"""
    import os
    return os.environ.get(key, default_value)


def get_sys_args(options=[], hint_text=None):
    import sys
    return get_args(argv=sys.argv[1:], options=options, hint_text=hint_text)


def get_sys_arg(short_option=None, long_option=None, default_value=None, hint_text=None):
    import sys
    key = 'SYS_ARG_KEY'
    options = [(key, short_option, long_option, default_value)]
    return get_args(argv=sys.argv[1:], options=options, hint_text=hint_text).get(key, default_value)


def get_args(argv, options=[], hint_text=None):
    import getopt
    import sys
    short_options = 'h' + ''.join(op[1] if op[1] else '' for op in options)
    long_options = ['help'] + [op[2] for op in options if op[2]]
    try:
        opts, other_args = getopt.getopt(argv, short_options, long_options)
    except getopt.GetoptError:
        if hint_text:
            print(f"usage: {hint_text}")
        sys.exit(2)

    args = {}
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            if hint_text:
                print(f"usage: {hint_text}")
            sys.exit()
        else:
            opt_key = opt.replace('-', '')
            for key, short_opt, long_opt, _ in options:
                if opt_key == short_opt.replace(':', '') or opt_key == long_opt.replace('=', ''):
                    args[key] = arg

    for key, _, _, default_value in options:
        if key not in args:
            args[key] = default_value

    return args


def get_param(
        key,
        config_file='config.json',
        default_value=None,
        type='str',
        log_enabled=True):
    import os
    import json
    from zlog2 import log

    def log_if_enabled(value):
        if log_enabled:
            log(f"{key}={value}")

    def translate_value(val):
        try:
            if type == 'bool':
                return bool(float(val))
            elif type == 'int':
                return int(float(val))
            elif type == 'float':
                return float(val)
            elif type == 'str':
                return str(val)
        except Exception as ex:
            print(f'get_param exception: {ex}')

        return val

    try:
        value = os.environ.get(key)
        if value:
            log_if_enabled(value)
            return translate_value(value)

        conf = json.loads(open(config_file, encoding='utf-8').read())
        value = conf.get(key)
        if value:
            log_if_enabled(value)
            return translate_value(value)
    except Exception as ex:
        print(f'get_param exception: {ex}')

    log_if_enabled(default_value)
    return default_value


def get_all_params(config_file='config.json', log_enabled=False):
    from zlog2 import log
    import json

    if log_enabled:
        log(f"=================环境变量读取开始=================")
    conf = json.loads(open(config_file, encoding='utf-8').read())
    for k, v in conf.items():
        conf[k] = get_param2(k, log_enabled=log_enabled)
    if log_enabled:
        log(f"=================环境变量读取结束=================")
    return conf


def get_param2(
        key,
        config_file='config.json',
        default_value=None,
        log_enabled=True):
    import os
    import json
    from zlog2 import log

    def log_if_enabled(value):
        if log_enabled:
            log(f"{key}={value}")

    def translate_value(val):
        try:
            if type(val) == bool:
                return bool(float(val))
            elif type(val) == int:
                return int(float(val))
            elif type(val) == float:
                return float(val)
            elif type(val) == str:
                return str(val)
        except Exception as ex:
            print(f'get_param exception: {ex}')

        return val

    def translate_value_with_type(val, type_val):
        try:
            if type(type_val) == bool:
                return bool(float(val))
            elif type(type_val) == int:
                return int(float(val))
            elif type(type_val) == float:
                return float(val)
            elif type(type_val) == str:
                return str(val)
        except Exception as ex:
            print(f'get_param exception: {ex}')

        return val

    try:
        conf = json.loads(open(config_file, encoding='utf-8').read())
        config_value = conf.get(key)

        value = os.environ.get(key)
        if value:
            log_if_enabled(value)
            return translate_value_with_type(value, config_value)

        if config_value:
            log_if_enabled(config_value)
            return translate_value(config_value)
    except Exception as ex:
        print(f'get_param exception: {ex}')

    log_if_enabled(default_value)
    return default_value


def main(argv):
    inputfile = ''
    outputfile = ''
    INPUT_FILE_KEY = 'input_file'
    OUTPUT_FILE_KEY = 'output_file'
    options = [
        (INPUT_FILE_KEY, 'i:', 'ifile=', '.'),
        (OUTPUT_FILE_KEY, 'o:', 'ofile=', '.')
    ]
    hint_text = '_.py -i <inputfile> -o <outputfile>'
    args = get_args(argv, options=options, hint_text=hint_text)

    print(f'参数: {args}')
    print('输入的文件为：', args.get(INPUT_FILE_KEY))
    print('输出的文件为：', args.get(OUTPUT_FILE_KEY))


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
