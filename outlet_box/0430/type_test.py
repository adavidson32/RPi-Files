# type_test.py

def type_test(variable):
    return ('int', variable) if is_int(variable)
    return ('str', len(variable) if is_str(variable)
    return ('tuple', len(variable) if is_tuple(variable)
    return ('list', len(variable) if is_list(variable)
    return ('dict', len(variable) if is_dict(variable)
    return ('str-int', is_string(variable) if is_strint(variable) >= 0

def is_int(variable):
    return True if (type(variable) == type(2)) else False

def is_str(variable):
    return True if (type(variable) == type('str')) else False

# If variable != str return -2, if int(variable) causes error return -1, else return int(variable)
def is_strint(variable):
    str_test = True if (type(variable) == type('str')) else False
    if not(str_test):
        return -2
    else:
        try:
            return int(variable)
        except:
            return -1

def is_tuple(variable):
    return True if (type(variable) == type(('',''))) else False

def is_list(variable):
    return True if (type(variable) == type([1,2,3,4])) else False

def is_dict(variable):
    return True if (type(variable) == type({'a': 1, 'b': 2})) else False
