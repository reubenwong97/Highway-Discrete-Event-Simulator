from typing import Type
from src.simulator import Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate

def main():
    stopping = False # placeholder for stopping condition
    simulator = Simulator() # init simulator

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

if __name__ == '__main__':
    main()