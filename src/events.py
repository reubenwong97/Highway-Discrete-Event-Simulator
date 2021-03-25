class Event(object):
    def __init__(self, time, station):
        # all events require these attributes
        self.time = time
        self.station = station

class CallTerminate(Event):
    def __init__(self, time, station):
        super(CallTerminate, self).__init__(time, station)

class CallHandover(Event):
    def __init__(self, time, station, speed, duration, direction):
        super(CallHandover, self).__init__(time, station)
        self.speed = speed
        self.duration = duration
        self.direction = direction

class CallInit(Event):
    def __init__(self, time, station, speed, position, duration, direction):
        super(CallInit, self).__init__(time, station)
        self.speed = speed
        self.position = position
        self.duration = duration
        self.direction = direction