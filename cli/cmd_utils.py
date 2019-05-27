import threading


class CmdUtils():

    '''
    Use:
        result = threaded(func, (param,))
    '''
    @staticmethod
    def threaded(func, args):
        class ThreadedResult():
            def __init__(self):
                self._has_result = False
                self._result     = None

            def set(self, val):
                if self._has_result:
                    raise ValueError('Cannot set result more than once')
                self._result = val
                self._has_result = True

            def get(self):
                if not self._has_result: 
                    raise ValueError('Threaded operation not finished')
                else: return self._result


        def wrap(func, args, result):
            result.set(func(*args))
                
            print('-----------------------')
            print('DONE')


        result = ThreadedResult()
        threading.Thread(target=wrap, args=(func, args, result)).start()
        return result


    # TODO
    @staticmethod
    def console_help():
        string = 'Available vars: \
            timeline, get_beatmap(), '

        #self.ipython_console.print_text('Available vars: ')