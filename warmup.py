from src.simulator import Simulator
from src.events import CallHandover, CallInit, CallTerminate
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from pathlib import Path

def main(args):
    check_path = Path(f'./results/warmups/res_{args.num_reserve}_blocked.npy')
    # capture stats
    blocked_arr = []
    dropped_arr = []
    num_inits = num_handover = num_terminate = 0
    if not check_path.exists():
        # set the base seed
        np.random.seed(args.seed)
        simulator = Simulator(args) # init simulator

        # for step in tqdm(range(args.steps), leave=False):
        for step in tqdm(range(args.steps)):
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

            blocked_arr.append((simulator.blocked_calls / simulator.total_calls)*100)
            dropped_arr.append((simulator.dropped_calls / simulator.total_calls)*100)        

        np.save(f'./results/warmups/res_{args.num_reserve}_blocked.npy', blocked_arr)
        np.save(f'./results/warmups/res_{args.num_reserve}_dropped.npy', dropped_arr)

    else:
        blocked_arr = np.load(f'./results/warmups/res_{args.num_reserve}_blocked.npy')
        dropped_arr = np.load(f'./results/warmups/res_{args.num_reserve}_dropped.npy')

    fig, ax = plt.subplots()

    ############################ UNUSED ########################
    # plt.plot(clock_times, blocked_percents, label='blocked')
    # plt.plot(clock_times, dropped_percents, label="dropped")
    # plt.xlabel('clock times')
    ############################################################

    ax.plot(blocked_arr, label='blocked')
    ax.plot(dropped_arr, label="dropped")
    ax.vlines(x=args.plot_at, ymin=-0.1, ymax=args.ymax, color='r', linestyle='dashed')
    ax.set_xlabel('Number of Events')
    ax.set_ylabel('Percentages')
    plt.legend()
    ax.set_title('Percentages of Dropped and Blocked Calls')

    fig.savefig(f'./images/warmups/res_{args.num_reserve}.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process simulation args')
    parser.add_argument('--num_reserve', default=0, type=int, help='The number of reserve channels')
    parser.add_argument('--num_stations', default=20, type=int, help='Number of stations along the highway')
    parser.add_argument('--seed', default=2021, type=int, help='Seed for seeding random values')
    parser.add_argument('--steps', default=700000, type=int, help='Steps taken in a single simulation run')
    parser.add_argument('--plot_at', default=600000, type=int, help='x-value at which to plot vline')
    parser.add_argument('--ymax', default=2.5, type=float, help='y-value at which to stop vline')
    args = parser.parse_args()

    main(args)