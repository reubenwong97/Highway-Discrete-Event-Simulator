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