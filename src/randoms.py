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
    def random_interarrival(beta=1.369817):
        u = np.random.uniform()
        return -beta * np.log(1 - u)
    
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
        Return uniform random number [0, 1] indicating relative position within a cell
        '''
        return np.random.uniform()

    @staticmethod
    def random_duration(beta=109.835901):
        u = np.random.uniform()
        return -beta * np.log(1 - u)

    @staticmethod
    def random_speed(mu=0.033353, std=0.002505):
        return np.random.normal(mu, std)

    @staticmethod
    def random_station(low=0, high=20):
        '''
        Returns "Discrete Uniform" variate. Excludes high
        '''
        return np.random.randint(low, high)