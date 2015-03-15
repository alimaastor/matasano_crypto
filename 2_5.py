
import random

def parse_structured_cookie(string):
    result = {}
    for pair in string.split('&'):
        key, value = pair.split('=')
        result[key] = value
    return result

def profile_for(string):
    return '&'.join(map(lambda x: '{}={}'.format(*x), {
        'email': string.translate(None, '&='),
        'uid': random.randint(0,500),
        'role': 'user',
    }.iteritems()))
