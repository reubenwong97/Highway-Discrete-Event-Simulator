from typing import Tuple, Type, Any
from src.events import CallHandover, CallInit, CallTerminate, Event
from src.randoms import Randoms

class FEL(list):
    def __init__(self):
        super(FEL, self).__init__()

    # comparator function
    def _compare_time(self, event: Event):
        return event.time

    # override list inserts
    # may be slow, maybe optimise later
    def insert(self, event: Event):
        if not isinstance(event, Event):
            raise TypeError
        super(FEL, self).append(event)
        super(FEL, self).sort(key=self._compare_time)

    def dequeue(self) -> Event:
        event = super(FEL, self).pop(0)
        return event

    def pop(self):
        raise Exception("Pop method should not be used, use dequeue() instead")

class CellStation(object):
    def __init__(self, station_id: int, with_reserve: bool, num_channels: int=10, coverage: int=2):
        self.station_id = station_id
        self.available_channels = num_channels
        if with_reserve:
            self.reserve_available = True # else no such attribute, good guard 
        self.range = [station_id * coverage, station_id * coverage + coverage] # cell_station coverage bounds

    def in_range(self, end_position):
        if end_position <= self.range[1] and end_position >= self.range[0]:
            return True
        return False    

class Simulator(object):
    def __init__(self, args):
        self.FEL = FEL() # investigate sorting by list -> list.sort(key=..., reverse=...)
        self.clock = 0
        self.stations_array = [CellStation(station_id=i, with_reserve=args.use_reserve) 
                                for i in range(args.num_stations)]

        random_interarrival = Randoms.random_time()
        first_call_time = random_interarrival
        speed, station_id, position, duration, direction = self.generate_args()
        first_call = CallInit(first_call_time, station_id, speed, position, duration, direction)

        self.FEL.insert(first_call)

        self.total_calls = 0
        self.dropped_calls = 0
        self.blocked_calls = 0

    def generate_args(self) -> Tuple:
        '''
        Helper function that helps to generate args for event instantiations.
        
            Args: None
            Returns:
                speed (float): int or float representing speed of car
                station (int): int representing station id
                position (float): float representing relative position
                duration (float): int representing duration of call
                direction (-1 / 1): -1 for left and 1 for right

        '''
        raise NotImplementedError
    
    def free_prev_station(self, current_station: int, direction: int, used_reserve: bool=False):
        '''
        Helper function to free up CellStation resource after usage.
        
            Args:
                current_station (int): CellStation.station_id caller is currently at
                direction (-1 / 1): Direction of travel
                used_reserve (bool): Indication of whether this call was made on a reserved channel or not
            Returns: None
        '''
        prev_station_id = current_station - direction
        if used_reserve:
            self.stations_array[prev_station_id].reserve_available = True
        else:
            self.stations_array[prev_station_id].available_channels += 1

    def compute_next_event(self, speed, position, duration, direction, 
    current_station: CellStation, current_event: Event) -> Tuple[str, int, int, Any, Any, Any]:
        '''
        Helper function for computing the next event.
            Args:
                speed (float): speed of car
                position (float): relative position wrt to current_station
                duration (float): duration of the call
                direction (1/-1): -1 for left and 1 for right
                current_station (CellStation): CellStation of current station. Reason for this datatype
                                               as opposed to int is due to the class attributes for convenience
                current_event (Event): Current event being processed. Holds useful attributes
            Returns:
                future_event_info (Tuple[str, int, int, Any, Any, Any]):
                    Tuple of information for the future event. Type, next_event_time and next_station_id are fixed returns. 
        '''
        total_distance = speed * duration
        absolute_position = (current_station.station_id + position) * current_station.range
        end_position = absolute_position + direction * total_distance
        next_station_id = current_station.station_id + direction

        if current_station.in_range(end_position) or next_station_id < 0 or next_station_id > 19:
            # if the call ends within current station or exceeds the highway, terminate
            termination_time = self.clock + duration
            # return termination flag for appropriate event generation
            return ("Termination", termination_time, current_station.station_id, None, None, None) # None returns for consistency
        
        boundary_index = max(0, direction)
        boundary_position = current_station.range[boundary_index]
        d = abs(absolute_position - boundary_position)
        #! Clarify on data type, this could easily be a non-integer
        time_to_next = d / speed
        remaining_duration = current_event.duration - time_to_next
        next_event_time = self.clock + time_to_next
        return ("Handover", next_event_time, next_station_id, speed, remaining_duration, direction)

    def handle_call_init(self, current_init):
        # process next initialisation event
        inter_arrival = Randoms.random_time()
        next_time = current_init.time + inter_arrival
        speed, station_id, position, duration, direction = self.generate_args()
        next_init = CallInit(next_time, station_id, speed, position, duration, direction)
        self.FEL.insert(next_init)

        # process current intialisation event
        if self.stations_array[current_init.station_id].available_channels == 0:
            self.blocked_calls += 1
        else:
            self.stations_array[current_init.station_id].available_channels -= 1
            speed, position, duration, direction = current_init.get_params()
            event_type, event_time, station_id, speed, remaining_duration, direction = \
                self.compute_next_event(speed, position, duration, direction, 
                    self.stations_array[current_init.station_id], current_init)
            if event_type == 'Terminate':
                termination_event = CallTerminate(event_time, station_id)
                self.FEL.insert(termination_event)
            else:
                assert event_type == 'Handover'
                handover_event = CallHandover(event_time, station_id, speed, remaining_duration, direction)
                self.FEL.insert(handover_event)
        self.total_calls += 1