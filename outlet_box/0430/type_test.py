# type_test.py

def type_test(variable):
    if is_int(variable):
        ret = ('int', variable)
    elif is_str(variable):
        ret = ('str', len(variable)
    elif is_tuple(variable):
        ret = ('tuple', len(variable)
    elif is_list(variable):
        ret = ('list', len(variable)
    elif is_dict(variable):
        ret = ('dict', len(variable)
    elif is_strint(variable):
        ret = ('str-int', int(variable)
    return ret

def is_int(variable):
    return True if (type(variable) == type(2)) else False

def is_str(variable):
    return True if (type(variable) == type('str')) else False

def is_strint(variable):
    str_test = True if (type(variable) == type('str')) else False
    if str_test:
        try:
            num = int(variable)
            return True
        except:
            return False
    else:
        return False

def is_tuple(variable):
    return True if (type(variable) == type(('',''))) else False

def is_list(variable):
    return True if (type(variable) == type([1,2,3,4])) else False

def is_dict(variable):
    return True if (type(variable) == type({'a': 1, 'b': 2})) else False
