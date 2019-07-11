import threading
import numpy as np


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


    @staticmethod
    def print_numbered_list(lst):
        for i in range(len(lst)):
            print(i, lst[i])


    @staticmethod
    def export_csv(name, data):
        data = np.asarray(data)
        if len(data) < 1: return
        
        size = len(data[0])
        csv_data  = ''

        for i in range(size):
             csv_data += ','.join([ str(x) for x in data[:,i] ]) + '\n'

        with open(name + '.txt', 'w') as csv_file:
            csv_file.write(csv_data)