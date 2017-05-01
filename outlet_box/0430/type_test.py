# type_test.py
# Use:
#   from type_test import type_test, is_int, is_float, is_str, is_strint....
#   some_string = '123'
#   some_number = int(some_string) if is_strint(some_string) else 'NaN'
#   if is_float(temp):
#       return round(temp, 2)

#------------------type_test Definition------------------------------

def type_test(variable, options='none'):
    if is_int(variable):
        ret = 'int'
    elif is_float(variable):
        ret = 'float'
    elif is_str(variable):
        ret = 'str'
    elif is_tuple(variable):
        ret = 'tuple'
    elif is_list(variable):
        ret = 'list'
    elif is_dict(variable):
        ret = 'dict'
    elif is_strint(variable):
        ret = 'str-int'
    if options == 'none':
        return ret
    elif options == 'len':
        var_len = 1 if (ret in ('int', 'str-int')) else len(variable)
        return (ret, var_len)
    elif options == 'value':
        if ret == 'str-int':
            return (ret, int(variable))
        else:
            return (ret, variable)
    elif options == 'str-num-split':
        if ret == 'str-int':
            str_ints = []
            for i in range(len(variable)):
                str_ints.append(int(variable[i]))
        else:
            str_ints = 'variable entered is not of str-int type...'
        return (ret, str_ints)

#-------------------Individual Type Tests----------------------------

def is_int(variable):
    return True if (type(variable) == type(2)) else False

def is_float(variable):
    return True if (type(variable) == type(0.253)) else False

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
