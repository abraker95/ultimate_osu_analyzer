
# Custom implementation of qt signal alternative
# because qt is retarded and doesn't support multiple inheritence
#
# Basically this is used as a decorator and adds a list of functions to the function.
# When emit is called, all the functions in the list are run
def callback(func):
    def Func(*args, **kwargs):
        return func(*args, **kwargs)
    
    class FuncHelper():
        @staticmethod
        def add_callback(callback):
            Func.callbacks.add(callback)
            return Func

        @staticmethod
        def rmv_callback(callback):
            try: Func.callbacks.remove(callback)
            except KeyError: pass
            return Func

        @staticmethod
        def exec_callbacks(*args, **kwargs):
            for callback in Func.callbacks.copy():
                if not Func.anti_recurse:
                    Func.anti_recurse = True
                    callback(*args, **kwargs)
                    Func.anti_recurse = False

            return Func

    # This is required or emiting from a function it is connected to will result in infinite recursion
    Func.anti_recurse = False
    
    Func.connect      = FuncHelper.add_callback
    Func.disconnect   = FuncHelper.rmv_callback
    Func.emit         = FuncHelper.exec_callbacks
    
    Func.callbacks = set()
    return Func