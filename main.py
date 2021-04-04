from typing import Type
from src.simulator import Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from run import run
import multiprocessing as mp
from functools import partial

def main(args):
    seeds = list(np.random.randint(1, 20381, size=args.reps))
    with mp.Manager() as manager:
        shared_blocked = manager.list()
        shared_dropped = manager.list()
        # processes = []

        run_func = partial(run, args, shared_blocked, shared_dropped)
        with mp.Pool(processes=4) as pool:
            pool.map(run_func, seeds)

        # for i in range(args.reps):
        #     p = mp.Process(target=run, args=(args, shared_blocked, shared_dropped, seeds[i]))
        #     p.start()
        #     processes.append(p)

        # [p.join() for p in processes]

        shared_blocked = list(shared_blocked)
        shared_dropped = list(shared_dropped)

        print(shared_blocked)
        print(shared_dropped)

        np.save(f'./results/reps_{args.reps}_blocked.npy', shared_blocked)
        np.save(f'./results/reps_{args.reps}_dropped.npy', shared_dropped)


    # fig, ax = plt.subplots()

    ############################ UNUSED ########################
    # plt.plot(clock_times, blocked_percents, label='blocked')
    # plt.plot(clock_times, dropped_percents, label="dropped")
    # plt.xlabel('clock times')
    ############################################################

    # ax.plot(blocked_percents, label='blocked')
    # ax.plot(dropped_percents, label="dropped")
    # ax.vlines(x=600000, color='r', linestyle='dashed')
    # ax.set_xlabel('Number of Events')
    # ax.set_ylabel('Percentages')
    # plt.legend()
    # ax.set_title('Percentages of Dropped and Blocked Calls')

    # fig.savefig(f'./images/{run_name}_stats.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process simulation args')
    parser.add_argument('--num_reserve', default=0, type=int, help='The number of reserve channels')
    parser.add_argument('--num_stations', default=20, type=int, help='Number of stations along the highway')
    parser.add_argument('--seed', default=2021, type=int, help='Seed for seeding random values')
    parser.add_argument('--warmup', default=600000, type=int, help='Number of steps to warm up a run')
    parser.add_argument('--steps', default=700000, type=int, help='Steps taken in a single simulation run')
    parser.add_argument('--reps', default=10, type=int, help='Number of repitions of simulation runs (n) in lectures')
    # parser.add_argument('--sets', default=10, type=int, help='Number of sets of repitions (m) in lectures')
    args = parser.parse_args()

    main(args)