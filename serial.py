from src.simulator import Simulator
from src.events import Event, CallHandover, CallInit, CallTerminate
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def main(args):
    # set the base seed
    np.random.seed(args.seed)
    final_blocked_arr = []
    final_dropped_arr = []
    seeds = list(np.random.randint(1, 20381, size=args.reps))
    print(f'Seeds: {seeds}')

    for rep in tqdm(range(args.reps)):
        np.random.seed(seeds[rep]) # scipy uses numpy seeds
        # print('Simulator initialised')
        args.seed = seeds[rep] # so simulator sets correct internal seed
        simulator = Simulator(args) # init simulator

        # capture stats
        blocked_arr = []
        dropped_arr = []
        num_inits = num_handover = num_terminate = 0
        warmed_up = False

        # for step in tqdm(range(args.steps), leave=False):
        for step in range(args.steps):
            # if step % 10000 == 0:
            #     print(f'Currently in step {step}')
            if step > args.warmup and not warmed_up:
                # print('Simulator reset')
                simulator.reset()
                warmed_up = True

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

            if warmed_up: # only start collecting when warmed up
                # print("total calls", simulator.total_calls)
                #! BUG FOUND, not the fault of the pool!!!
                # I had just reset and then entered this section where I attempt to divide by 0
                assert simulator.total_calls != 0
                percent_blocked = (simulator.blocked_calls / simulator.total_calls) * 100
                percent_dropped = (simulator.dropped_calls / simulator.total_calls) * 100
                blocked_arr.append(percent_blocked)
                dropped_arr.append(percent_dropped)

        final_blocked_arr.append(np.mean(blocked_arr))
        final_dropped_arr.append(np.mean(dropped_arr))        

    np.save(f'./results/reps_{args.reps}_blocked.npy', final_blocked_arr)
    np.save(f'./results/reps_{args.reps}_dropped.npy', final_dropped_arr)


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
    args = parser.parse_args()

    main(args)