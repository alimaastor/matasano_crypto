
import random

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

def get_random_length_text(length=16):
    return reduce(lambda x,_: x + chr(random.randint(0,255)),xrange(random.randint(0,length)),'')

def get_random_text(length=16):
    return reduce(lambda x,_: x + chr(random.randint(0,255)),xrange(length),'')