from typing import Tuple, Type, Any
from src.events import CallHandover, CallInit, CallTerminate, Event
from src.randoms import Randoms

class FEL(list):
    def __init__(self):
        super(FEL, self).__init__()

    # comparator function
    def _compare_time(self, event: Event) -> float:
        return event.time

    # override list inserts
    # sorts should be fast since list typically doesnt get too large
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
    # edited CellStation to allow for multiple reserve channels
    def __init__(self, station_id: int, num_reserve: int, num_channels: int=10, coverage: int=2):
        self.station_id = station_id
        # available normal channels
        self.available_channels = num_channels - num_reserve
        self.coverage = coverage
        if num_reserve != 0:
            self.free_reserve = num_reserve # else no such attribute, good guard 
        self.range = [station_id * coverage, station_id * coverage + coverage] # cell_station coverage bounds

    def in_range(self, end_position):
        if end_position <= self.range[1] and end_position >= self.range[0]:
            return True
        return False 
    
    def reserve_available(self):
        if self.free_reserve > 0:
            return True
        return False

class Simulator(object):
    def __init__(self, args):
        self.FEL = FEL() # investigate sorting by list -> list.sort(key=..., reverse=...)
        self.clock = 0
        self.stations_array = [CellStation(station_id=i, num_reserve=args.num_reserve) 
                                for i in range(args.num_stations)]
        self.rng = Randoms(args.seed)

        random_interarrival = self.rng.random_interarrival()
        first_call_time = random_interarrival
        speed, station_id, position, duration, direction = self.generate_args()
        first_call = CallInit(first_call_time, station_id, speed, position, duration, direction)

        self.FEL.insert(first_call)

        self.total_calls = 0
        self.dropped_calls = 0
        self.blocked_calls = 0

        # for debugging
        self.init_handover = 0
        self.handover_handover = 0

    def reset(self):
        self.total_calls = 0 # no longer counting step-by-step, offset not required
        self.dropped_calls = 0
        self.blocked_calls = 0

    def generate_args(self) -> Tuple[float, int, float, float, int]:
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
        return (self.rng.random_speed(), self.rng.random_station(), self.rng.random_position(),
            self.rng.random_duration(), self.rng.random_direction())

    def free_current_station(self, current_station: int, used_reserve: bool=False):
        '''
        Helper function to free up CellStation resource after usage. Used by Termination handler.
            Args:
                current_station (int): CellStation.station_id caller is currently at, and station to free
                used_reserve (bool): Indication of whether this call was made on a reserved channel or not
            Returns: None
        '''
        if used_reserve:
            self.stations_array[current_station].free_reserve += 1
        else:
            self.stations_array[current_station].available_channels += 1
    
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
            # implemented as int for generality
            self.stations_array[prev_station_id].free_reserve += 1
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
        absolute_position = (current_station.station_id + position) * current_station.coverage
        end_position = absolute_position + direction * total_distance
        next_station_id = current_station.station_id + direction
        
        boundary_index = max(0, direction)
        boundary_position = current_station.range[boundary_index]
        d = abs(absolute_position - boundary_position)
        time_to_next = d / speed # time can be float
        remaining_duration = current_event.duration - time_to_next
        next_event_time = self.clock + time_to_next

        #! Repositioned after time checking
        if current_station.in_range(end_position) or next_station_id < 0 or next_station_id > 19 or \
            remaining_duration <= 0: # additional guard just in case (but should be caught by end_position)
            # if the call ends within current station or exceeds the highway, terminate
            termination_time = next_event_time
            # return termination flag for appropriate event generation
            return ("Terminate", termination_time, current_station.station_id, None, None, None) # None returns for consistency

        return ("Handover", next_event_time, next_station_id, speed, remaining_duration, direction)

    def handle_call_init(self, current_init):
        # process next initialisation event
        assert self.clock == current_init.time # assert advancement of clock
        inter_arrival = self.rng.random_interarrival()
        next_time = current_init.time + inter_arrival
        speed, station_id, position, duration, direction = self.generate_args()
        next_init = CallInit(next_time, station_id, speed, position, duration, direction)
        self.FEL.insert(next_init)

        # process current intialisation event
        # available channels are handled seperately from reserved channels
        # i.e. if the available_channels = 10 - num_reserve
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
                self.init_handover += 1
                handover_event = CallHandover(event_time, station_id, speed, remaining_duration, direction)
                self.FEL.insert(handover_event)
        self.total_calls += 1 # as long as they tried, call attempt made

    def handle_call_handover_no_res(self, current_handover):
        assert self.clock == current_handover.time
        # get current info for DOING handover
        speed, station_id, duration, direction = current_handover.get_params()
        position = 1 if direction == -1 else 0 # when handing over, position is always at a bound
        self.free_prev_station(station_id, direction, used_reserve=False)

        if self.stations_array[station_id].available_channels == 0:
            self.dropped_calls += 1
        else:
            self.stations_array[station_id].available_channels -= 1
            event_type, event_time, station, speed, remaining_duration, direction = \
                self.compute_next_event(speed, position, duration, direction, self.stations_array[station_id],
                    current_handover)
            if event_type == "Terminate":
                termination_event = CallTerminate(event_time, station)
                self.FEL.insert(termination_event)
            elif event_type == "Handover":
                self.handover_handover += 1
                handover_event = CallHandover(event_time, station, speed, remaining_duration, direction)
                self.FEL.insert(handover_event)
            else:
                raise TypeError("Wrong event type returned")
        
    def handle_call_handover_res(self, current_handover):
        assert self.clock == current_handover.time
        speed, station_id, duration, direction = current_handover.get_params()
        position = 1 if direction == -1 else 0
        used_reserve = getattr(current_handover, "used_reserve", False)
        self.free_prev_station(station_id, direction, used_reserve=used_reserve)

        # when call is blocked
        if self.stations_array[station_id].available_channels == 0 and \
            (not self.stations_array[station_id].reserve_available()): # reserve available if I have > 0 reserve available
            self.dropped_calls += 1
        # One type of channel is available, find out which
        else:
            # no free regular channels, use reserved channels
            if self.stations_array[station_id].available_channels == 0:
                self.stations_array[station_id].free_reserve -= 1
                used_reserve = True
            # regular channels available
            else:
                self.stations_array[station_id].available_channels -= 1
                used_reserve = False
            # accepted call with known channel type now to be processed
            event_type, event_time, station, speed, remaining_duration, directon = \
                self.compute_next_event(speed, position, duration, direction, self.stations_array[station_id],
                    current_handover)
            if event_type == "Terminate":
                termination_event = CallTerminate(event_time, station, used_reserve)
                self.FEL.insert(termination_event)
            elif event_type == "Handover":
                handover_event = CallHandover(event_time, station, speed, remaining_duration, direction, used_reserve)
                self.FEL.insert(handover_event)

    def handle_call_termination(self, current_termination):
        assert self.clock == current_termination.time
        _, station_id = current_termination.get_params()
        used_reserve = getattr(current_termination, "used_reserve", False)
        self.free_current_station(station_id, used_reserve)