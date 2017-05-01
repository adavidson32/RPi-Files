# type_test.py

def type_test(variable, ret_len=0):
    if type(variable) == type(2):
        return 'int'
    else:
        if type(variable) == type('str'):
            ret = 'str'
        elif type(variable) == type(('',)):
            ret = 'tuple'
        elif type(variable) == type([1,2,3,4]):
            ret = 'list'
        elif type(variable) == type(1.234):
            ret = 'float'
        elif type(variable) == type({'a': 1, 'b': 2}):
            ret = 'dict'
        if ret_len:
            var_len = len(variable)
            return (ret, var_len)
        else:
            return ret
