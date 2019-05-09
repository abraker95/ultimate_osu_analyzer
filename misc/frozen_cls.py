from functools import wraps


'''
Name: Frozen Class
Description:
    Freezes the class's attributes; Prohibits other classes from setting new attributes for this class
    Ensures all attributes that the class may have are declared as part of the class's definition and in __init__ beforehand
    To be used as a class decorator
Note: If a class has a base class that is a Frozen Class, then it needs to be initialized after setting the derived class's attributes
'''
# Thanks https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init/29368642#29368642
def FrozenCls(cls):

    def init(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.__frozen = False
            func(self, *args, **kwargs)
            self.__frozen = True
        
        return wrapper


    def frozen_setattr(self, name, value):
        if not self.__frozen or hasattr(self, name):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError('Please declare %s in %s\'s __init__ before setting it from elsewhere.' % (name, cls.__name__))

    cls.__frozen    = False
    cls.__setattr__ = frozen_setattr
    cls.__init__    = init(cls.__init__)

    return cls
