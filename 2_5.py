
import random
from collections import OrderedDict

def parse_structured_cookie(string):
    result = {}
    for pair in string.split('&'):
        key, value = pair.split('=')
        result[key] = value
    return result

def profile_for(string):
    r = OrderedDict()
    r['email'] = string.translate(None, '&=')
    r['uid']   = 15
    r['role']  = 'user'
    return '&'.join(map(lambda x: '{}={}'.format(*x), r.iteritems()))
