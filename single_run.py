from typing import Type
from src.simulator import Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def main(args):
    run_name = 'no_res' if args.num_reserve == 0 else str(args.num_reserve)+'res'
    np.random.seed(args.seed)
    simulator = Simulator(args) # init simulator

    # capture stats
    blocked_arr = []
    dropped_arr = []
    num_inits = num_handover = num_terminate = 0

    for step in tqdm(range(0, args.steps), leave=False):
        event = simulator.FEL.dequeue()
        simulator.clock = event.time # advance clock to event
        # clock_times.append(simulator.clock)

        if isinstance(event, CallInit):
            simulator.handle_call_init(event)
            num_inits += 1
        elif isinstance(event, CallHandover):
            num_handover += 1
            if args.num_reserve == 0:
                simulator.handle_call_handover_no_res(event)
            else:
                simulator.handle_call_handover_res(event)
        elif isinstance(event, CallTerminate):
            num_terminate += 1
            simulator.handle_call_termination(event)
        else:
            raise TypeError("Wrong event type in FEL")

        percent_blocked = (simulator.blocked_calls / simulator.total_calls) * 100
        percent_dropped = (simulator.dropped_calls / simulator.total_calls) * 100
        blocked_arr.append(percent_blocked)
        dropped_arr.append(percent_dropped)

    # Handover count discrepancy could be due to simulation terminating since I count handovers when they are dequeued
    # and count the transitions when created
    # print(f"""Inits: {num_inits}, Handovers: {num_handover}, Terminates: {num_terminate}, Blocked: {simulator.blocked_calls} 
    #           Dropped: {simulator.dropped_calls}, Init2Handover: {simulator.init_handover}, Handover2Handover: {simulator.handover_handover}
    #           Length of FEL: {len(simulator.FEL)}""")

    # placeholder for stats
    np.save(f'./results/{run_name}_blocked.npy', blocked_arr)
    np.save(f'./results/{run_name}_dropped.npy', dropped_arr)

    # blocked_percents = list(map(lambda x: x*100, blocked_arr))
    # dropped_percents = list(map(lambda x: x*100, dropped_arr))

    fig, ax = plt.subplots()

    ############################ UNUSED ########################
    # plt.plot(clock_times, blocked_percents, label='blocked')
    # plt.plot(clock_times, dropped_percents, label="dropped")
    # plt.xlabel('clock times')
    ############################################################

    ax.plot(blocked_arr, label='blocked')
    ax.plot(dropped_arr, label="dropped")
    ax.vlines(x=600000, ymin=0, ymax=2.5, color='r', linestyle='dashed')
    ax.set_xlabel('Number of Events')
    ax.set_ylabel('Percentages')
    plt.legend()
    ax.set_title('Percentages of Dropped and Blocked Calls')

    fig.savefig(f'./images/{run_name}_stats.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process simulation args')
    parser.add_argument('--num_reserve', default=0, type=int, help='The number of reserve channels')
    parser.add_argument('--num_stations', default=20, type=int, help='Number of stations along the highway')
    parser.add_argument('--seed', default=2021, type=int, help='Seed for seeding random values')
    parser.add_argument('--steps', default=700000, type=int, help='Steps taken in a single simulation run')
    args = parser.parse_args()

    main(args)