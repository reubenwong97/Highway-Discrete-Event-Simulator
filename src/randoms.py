import numpy as np

class Randoms(object):
    __instance__ = None

    def __init__(self):
        if Randoms.__instance__ is None:
            Randoms.__instance__ = self
        else:
            raise Exception("Cannot create another SingletonEventHandler class")

    @staticmethod
    def get_instance():
        if not Randoms.__instance__:
            Randoms()
        return Randoms.__instance__

    @staticmethod
    def random_time():
        raise NotImplementedError
    
    @staticmethod
    def random_direction():
        '''
        2-point distribution with probability 0.5 each
        '''
        if np.random.random() < 0.5:
            return -1
        else:
            return 1

    @staticmethod
    def random_position():
        '''
        Return uniform random number [0, 1) indicating relative position within a cell
        '''
        return np.random.random()