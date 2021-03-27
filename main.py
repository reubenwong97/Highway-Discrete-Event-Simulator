from typing import Type
from src.simulator import Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate
import argparse

def main(args):
    stopping = False # placeholder for stopping condition
    simulator = Simulator(args) # init simulator

    while not stopping:
        event = simulator.FEL.dequeue()
        clock = event.time

        if isinstance(event, CallInit):
            pass
        elif isinstance(event, CallHandover):
            pass
        elif isinstance(event, CallTerminate):
            pass
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