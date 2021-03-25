from typing import Type
from src.events import Event

class FEL(list):
    def __init__(self):
        super(FEL, self).__init__()

    # override list inserts
    # may be slow, maybe optimise later
    def insert(self, event):
        if not isinstance(event, Event):
            raise TypeError
        super(FEL, self).append(event)
        super(FEL, self).sort(key=event.time)

    # override for index consistency
    def pop(self):
        event = super(FEL, self).pop(0)

        return event

class CellStation(object):
    def __init__(self, station_id , with_reserve, num_channels=10):
        self.station_id = station_id
        self.available_channels = num_channels

class Simulator(object):
    def __init__(self, args):
        self.FEL = FEL() # investigate sorting by list -> list.sort(key=..., reverse=...)
        self.clock = 0
        self.stations_array = [CellStation(station_id=i, with_reserve=args.use_reserve) for i in range(args.num_stations)]