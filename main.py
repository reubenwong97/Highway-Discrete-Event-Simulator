from typing import Type
from src.simulator import Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate
import argparse

def main(args):
    stopping = False # placeholder for stopping condition
    simulator = Simulator(args) # init simulator

    while not stopping:
        event = simulator.FEL.dequeue()
        simulator.clock = event.time # advance clock to event

        if isinstance(event, CallInit):
            simulator.handle_call_init(event)
        elif isinstance(event, CallHandover):
            if args.num_reserve == 0:
                simulator.handle_call_handover_no_res(event)
            else:
                simulator.handle_call_handover_res(event)
        elif isinstance(event, CallTerminate):
            simulator.handle_call_termination(event)
        else:
            raise TypeError("Wrong event type in FEL")

    percent_blocked = simulator.blocked_calls / simulator.total_calls
    percent_dropped = simulator.dropped_calls / simulator.total_calls

    # placeholder for stats
    print(percent_blocked, percent_dropped)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process simulation args')
    parser.add_argument('--num_reserve', default=0, type=int)
    parser.add_argument('--num_stations', default=20, type=int)
    args = parser.parse_args()

    main(args)