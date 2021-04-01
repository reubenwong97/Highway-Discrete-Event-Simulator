from typing import Type
from src.simulator import Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def main(args):
    np.random.seed(args.seed)
    simulator = Simulator(args) # init simulator

    blocked_arr = []
    dropped_arr = []

    for i in tqdm(range(0, 150000)):
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
        blocked_arr.append(percent_blocked)
        dropped_arr.append(percent_dropped)

    # placeholder for stats
    np.save('./results/blocked.npy', blocked_arr)
    np.save('./results/dropped.npy', dropped_arr)

    fig = plt.figure()
    plt.plot(blocked_arr, label='blocked')
    plt.plot(dropped_arr, label="dropped")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process simulation args')
    parser.add_argument('--num_reserve', default=0, type=int)
    parser.add_argument('--num_stations', default=20, type=int)
    parser.add_argument('--seed', default=2021, type=int)
    args = parser.parse_args()

    main(args)