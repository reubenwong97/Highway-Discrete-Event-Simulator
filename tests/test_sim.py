from src.simulator import FEL, Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate

def test_FEL_list_subclassing():
    event_list = FEL()
    assert len(event_list) == 0

    event_list.append(5)
    assert event_list[0] == 5

def test_event_types():
    handover = CallHandover(1, 1, 1, 1, 1)
    Init = CallInit(1, 1, 1, 1, 1, 1)
    Terminate = CallTerminate(1, 1)

    assert isinstance(handover, Event)
    assert isinstance(Init, Event)
    assert isinstance(Terminate, Event)

def test_event_attributes():
    handover = CallHandover(5, 1, 1, 1, 1)

    assert handover.time == 5

def test_event_insertion():
    event_list = FEL()
    terminate = CallTerminate(10, 1)
    handover = CallHandover(5, 1, 1, 1, 1)
    init = CallInit(3, 1, 1, 1, 1, 1)

    event_list.insert(handover)
    event_list.insert(terminate)
    event_list.insert(init)

    assert isinstance(event_list[0], CallInit)
    assert isinstance(event_list[1], CallHandover)
    assert isinstance(event_list[2], CallTerminate)

def test_event_dequeue():
    event_list = FEL()
    terminate = CallTerminate(10, 1)
    handover = CallHandover(5, 1, 1, 1, 1)
    init = CallInit(3, 1, 1, 1, 1, 1)

    event_list.insert(handover)
    event_list.insert(terminate)
    event_list.insert(init)

    original_len = len(event_list)
    new_len = original_len -1
    event = event_list.dequeue()

    assert len(event_list) == new_len
    assert isinstance(event, CallInit)

def test_get_attr():
    terminate = CallTerminate(10, 1)
    handover = CallHandover(5, 1, 1, 1, 1)
    init = CallInit(3, 1, 1, 1, 1, 1)

    assert terminate.get_params() == (10, 1)
    assert handover.get_params() == (1, 1, 1, 1)
    assert init.get_params() == (1, 1, 1, 1)

def test_event_computation():
    import argparse
    # args = {
    #     'use_reserve': False,
    #     'num_stations': 20
    # }
    parser = argparse.ArgumentParser(description='Process simulation args')
    parser.add_argument('--use_reserve', default=False, type=bool)
    parser.add_argument('--num_stations', default=20, type=int)
    args = parser.parse_args()

    simulator = Simulator(args)
    current_init = CallInit(0, 0, 1, 0, 0.5, 1)
    speed, position, duration, direction = current_init.get_params()
    next_event_type, _, _, _, _, _ = simulator.compute_next_event(speed, position, duration, direction, 
        simulator.stations_array[current_init.station_id], current_init)

    assert next_event_type == "Termination"