
# Custom implementation of qt signal alternative
# because qt is retarded and doesn't support multiple inheritence
#
# Basically this is used as a decorator and adds a list of functions to the function.
# When emit is called, all the functions in the list are run. Their returns are collected
#     into Func.returns as the function execute
# NOTE: The when a function is connected to another function, the connection applies to all
#     instances of the class the function is defined in
def callback(func):

    def Func(*args, **kwargs):
        return func(*args, **kwargs)
    
    class FuncHelper():

        @staticmethod
        def add_callback(callback, inst=None):
            if not inst in Func.callbacks:
                Func.callbacks[inst] = set()
            
            Func.callbacks[inst].add(callback)
            return Func

        @staticmethod
        def rmv_callback(callback, inst=None):
            try: Func.callbacks[inst].remove(callback)
            except KeyError: pass
            return Func

        @staticmethod
        def exec_callbacks(*args, inst=None, **kwargs):
            if not inst in Func.callbacks: return Func

            Func.returns = {}
            # Copy because one of the callbacks can be a disconnect to the refered callbacks
            # This would effectively change the size of Func.callbacks, causing an exception
            for callback in Func.callbacks[inst].copy():
                if Func.anti_recurse: continue
                
                Func.anti_recurse = True
                Func.returns[callback] = callback(*args, **kwargs)
                Func.anti_recurse = False

            return Func

        @staticmethod 
        def get_return_for(callback):
            if not callback in Func.returns: return None
            else: return Func.returns[callback]

    # This is required to ensure emiting from a function it is connected to
    # will not result in infinite recursion via self reference. This causes
    # the connected function to only execute one time from per specific function's emit
    Func.anti_recurse = False
    Func.returns      = {}

    Func.connect      = FuncHelper.add_callback
    Func.disconnect   = FuncHelper.rmv_callback
    Func.emit         = FuncHelper.exec_callbacks
    Func.ret          = FuncHelper.get_return_for
    
    Func.callbacks = {}
    return Func