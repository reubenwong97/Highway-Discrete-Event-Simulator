from typing import Type
from src.simulator import Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from src.runner import run
import multiprocessing as mp
from functools import partial
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def main(args):
    # NOTE: tests had been run to ensure that running in parallel gives the same results as serial
    # set the base seeds so seeds are consistent
    np.random.seed(args.seed)
    seeds = list(np.random.randint(1, 20381, size=args.reps))
    print(f'Seeds: {seeds}')
    processes = []
    # global_count = mp.Value('i', 0)
    with mp.Manager() as manager:
        shared_blocked = manager.list()
        shared_dropped = manager.list()

        run_func = partial(run, args, shared_blocked, shared_dropped)
        with mp.get_context('spawn').Pool(processes=args.workers) as pool:
            assert len(seeds) == args.reps
            pool.map(run_func, seeds)

        shared_blocked = list(shared_blocked)
        shared_dropped = list(shared_dropped)

        print(shared_blocked)
        print(shared_dropped)

        results_dir = Path(f'./results/reserve_{args.num_reserve}/')
        if not Path.is_dir(results_dir):
            results_dir.mkdir(parents=True) # create paths as necessary
        np.save(f'./results/reserve_{args.num_reserve}/reps_{args.reps}_blocked.npy', shared_blocked)
        np.save(f'./results/reserve_{args.num_reserve}/reps_{args.reps}_dropped.npy', shared_dropped)


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
    mp.set_start_method('spawn')

    parser = argparse.ArgumentParser(description='Process simulation args')
    parser.add_argument('--num_reserve', default=0, type=int, help='The number of reserve channels')
    parser.add_argument('--num_stations', default=20, type=int, help='Number of stations along the highway')
    parser.add_argument('--seed', default=2021, type=int, help='Seed for seeding random values')
    parser.add_argument('--warmup', default=600000, type=int, help='Number of steps to warm up a run')
    parser.add_argument('--steps', default=700000, type=int, help='Steps taken in a single simulation run')
    parser.add_argument('--reps', default=10, type=int, help='Number of repitions of simulation runs (n) in lectures')
    parser.add_argument('--workers', default=6, type=int, help='Number of workers to run in parallel')
    args = parser.parse_args()

    main(args)