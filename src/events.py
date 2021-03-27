class Event(object):
    def __init__(self, time, station_id):
        # all events require these attributes
        self.time = time
        #! STANDARDISE ALL TO ID 
        self.station_id = station_id

    def get_params(self):
        return [v for k, v in self.__dict__.items() if '__' not in k and 'object at' not in k]

class CallTerminate(Event):
    def __init__(self, time, station_id, used_reserve=False):
        super().__init__(time, station_id)

    def get_params(self):
        return self.time, self.station_id

class CallHandover(Event):
    def __init__(self, time, station_id, speed, duration, direction, used_reserve=False):
        super().__init__(time, station_id)
        self.speed = speed
        self.duration = duration
        self.direction = direction
        self.used_reserve = used_reserve

    def get_params(self):
        # if self.used_reserve:
        #     return self.speed, self.station_id, self.duration, self.direction, self.used_reserve
        # else:
        # At the moment, access used_reserve with getattr
        return self.speed, self.station_id, self.duration, self.direction

class CallInit(Event):
    def __init__(self, time, station_id, speed, position, duration, direction):
        super().__init__(time, station_id)
        self.speed = speed
        self.position = position
        self.duration = duration
        self.direction = direction

    def get_params(self):
        return self.speed, self.position, self.duration, self.direction