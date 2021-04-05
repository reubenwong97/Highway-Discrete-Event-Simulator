from src.simulator import Simulator
from src.events import CallHandover, CallInit, CallTerminate
import numpy as np

def run(args, shared_blocked, shared_dropped, run_seed):
    np.random.seed(run_seed) # scipy uses numpy seeds
    args.seed = run_seed
    simulator = Simulator(args) # init simulator

    # capture stats
    blocked_arr = []
    dropped_arr = []
    num_inits = num_handover = num_terminate = 0
    warmed_up = False

    for step in range(args.steps):
        if step > args.warmup and not warmed_up:
            # print('Simulator reset')
            simulator.reset()
            warmed_up = True

        event = simulator.FEL.dequeue()
        simulator.clock = event.time # advance clock to event

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
            assert simulator.total_calls != 0
            percent_blocked = (simulator.blocked_calls / simulator.total_calls) * 100
            percent_dropped = (simulator.dropped_calls / simulator.total_calls) * 100
            blocked_arr.append(percent_blocked)
            dropped_arr.append(percent_dropped)

    mean_blocked = np.mean(blocked_arr)
    mean_dropped = np.mean(dropped_arr)

    # store results in shared list
    shared_blocked.append(mean_blocked)
    shared_dropped.append(mean_dropped)