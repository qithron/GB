'''
FUF (Frequently Used Functions) aka Shortcuts.
'''

def all_elem(iterable):
    return False if iterable and iterable.count(iterable[0]) != len(iterable)\
    else True

def any_elem(iterable):
    for element in iterable:
        if iterable.count(element) > 1:
            return True
    return False

def any_float(iterable):
    for element in iterable:
        if type(element) == float:
            return True
    return False

def all_float(iterable):
    for element in iterable:
        if type(element) != float:
            return False
    return True

def any_int(iterable):
    for element in iterable:
        if type(element) == int:
            return True
    return False

def all_int(iterable):
    for element in iterable:
        if type(element) != int:
            return False
    return True

def is_int(x):
    return True if type(x) == int else (x).is_integer()

def is_num(obj):
    return True if type(obj) == int or type(obj) == float \
    else False

def int_try(obj):
    if type(obj) == int:
        return obj
    elif type(obj) == float:
        return int(obj) if is_int(obj) else obj
    return tuple([int(x) if is_int(x) else x for x in obj])

def xor(a, b):
    return bool(a^b)
