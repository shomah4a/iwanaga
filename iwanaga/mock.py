#-*- coding:utf-8 -*-
'''
mocking module
'''

import functools
import types


class Mock(object):
    '''
    Mocking class used with with_statement.
    '''

    def __init__(self, table):
        '''
        構築子

        :param table: replace information
        :type table: (str, object)        
        '''

        if isinstance(table, dict):
            table = table.iteritems()

        self.table = table


    def decorator(self, f):
        '''
        mock
        '''

        return mocking(self)(f)


    __call__ = decorator


    def mocking(self):

        return MockScope(self)




def load_module(name):

    mod = __import__(name)

    sp = name.split('.')


    return get_module(mod, sp[1:])



def get_module(obj, path):

    if not path:
        return obj

    cur = path[0]
    left = path[1:]

    return get_module(getattr(obj, cur), left)
    


def replace_recursive(obj, namespaces, value):

    if not namespaces:
        raise ValueError, 'invalid target name'

    cur = namespaces[0]

    if len(namespaces) == 1:

        ret = getattr(obj, cur)
        setattr(obj, cur, value)

        return ret

    left = namespaces[1:]

    return replace_recursive(getattr(obj, cur), left, value)




def replace(path, value):

    mod, name = path.split(':')

    mod = load_module(mod)

    return replace_recursive(mod, name.split('.'), value)



class MockScope(object):
    '''
    with で使われるっぽい
    '''

    def __init__(self, mock):
        '''
        構築子
        '''
        self.mock = mock
    

    def __enter__(self):

        self.cache = []

        for k, v in self.mock.table:

            self.cache.append((k, replace(k, v)))



    def __exit__(self, *args):
        
        for k, v in self.cache:

            replace(k, v)



def mock(path):

    if isinstance(path, types.ModuleType):
        path = path.__name__


    def mocking(f):

        name = '%s:%s' % (path, f.__name__)

        return Mock([(name, f)])

    return mocking



def mocking(arg):

    if isinstance(arg, Mock):
        mock = arg
    else:
        mock = Mock(arg)

    def decorator(f):

        @functools.wraps(f)
        def do_mocking(*args, **argd):

            with mock.mocking():
                return f(*args, **argd)

        return do_mocking

    return decorator

