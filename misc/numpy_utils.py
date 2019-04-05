import numpy as np


class NumpyUtils():

    @staticmethod
    def dists(x_list, y_list):
        if len(x_list) < 1 or len(y_list) < 1: return np.array([])
        return np.sqrt((x_list[:,0] - y_list[:,0])**2 + (x_list[:,1] - y_list[:,1])**2)


    @staticmethod
    def deltas(lst):
        return lst[1:] - lst[:-1]


    @staticmethod
    def func(func, lst):
        if len(lst) < 1: return None
        return [ func(param) for param in zip(*lst) ]


    @staticmethod
    def first(lst):
        try: return lst[0]
        except: return None

    
    @staticmethod
    def last(lst):
        try: return lst[-1]
        except: return None