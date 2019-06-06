import cgi
import fcntl

from datetime import datetime

from .parameters import parameters


def get_parameters(keys, replace_none_with_empty_strings=False):
    result = {}
    for key in keys:
        value = parameters.getfirst(key)
        if value is None and replace_none_with_empty_strings:
            value = ''
        result[key] = value
    return result


def sanitize_for_csv(value):
    text = str(value).replace('\r', ' ').replace('\n', ' ').replace('"', '""')
    return f'"{text}"'


def get_csv_row(keys):
    values = (datetime.today(),) + tuple(parameters.getfirst(key) for key in keys)
    return f'{",".join(sanitize_for_csv(value) for value in values)}\n'


def save_to_csv(path, keys):
    with open(path, mode='a', encoding='utf-8') as csv_file:
        fcntl.lockf(csv_file, fcntl.LOCK_EX)
        csv_file.write(get_csv_row(keys))
