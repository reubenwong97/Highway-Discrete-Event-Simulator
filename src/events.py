class Event(object):
    def __init__(self, time, station_id):
        # all events require these attributes
        self.time = time
        #! STANDARDISE ALL TO ID 
        self.station_id = station_id

    def get_params(self):
        return [v for k, v in self.__dict__.items() if '__' not in k and 'object at' not in k]
class CallTerminate(Event):
    def __init__(self, time, station):
        super().__init__(time, station)

class CallHandover(Event):
    def __init__(self, time, station, speed, duration, direction):
        super().__init__(time, station)
        self.speed = speed
        self.duration = duration
        self.direction = direction

class CallInit(Event):
    def __init__(self, time, station, speed, position, duration, direction):
        super().__init__(time, station)
        self.speed = speed
        self.position = position
        self.duration = duration
        self.direction = direction

    def get_params(self):
        return self.speed, self.position, self.duration, self.direction