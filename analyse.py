import numpy as np
import argparse

def analyse(args):
    dropped_name = f'./results/reserve_{args.num_reserve}/reps_{args.reps}_dropped.npy'
    blocked_name = f'./results/reserve_{args.num_reserve}/reps_{args.reps}_blocked.npy'
    out_file = f'./results/text_results/reserve_{args.num_reserve}_reps_{args.reps}_summary.txt'
    
    dropped_arr = np.load(dropped_name)
    blocked_arr = np.load(blocked_name)

    assert len(dropped_arr) == args.reps
    assert len(blocked_arr) == args.reps

    mean_dropped = np.mean(dropped_arr)
    mean_blocked = np.mean(blocked_arr)

    var_dropped = np.sum((dropped_arr-mean_dropped)**2) / (len(dropped_arr)-1)
    var_blocked = np.sum((blocked_arr-mean_blocked)**2) / (len(blocked_arr)-1)
    
    with open(out_file, 'w') as f:
        f.write('Displaying arrays\n')
        f.write(f'Drop array: {dropped_arr}\n')
        f.write(f'Block array: {blocked_arr}\n')
        f.write('Displaying statistics\n')
        f.write(f'Mean drop rate: {mean_dropped}\n')
        f.write(f'Variance of drop rate: {var_dropped}\n')
        f.write(f'Standard deviation of drop rate: {np.sqrt(var_dropped)}\n')
        f.write(f'Mean of block rate: {mean_blocked}\n')
        f.write(f'Variance of block rate: {var_blocked}\n')
        f.write(f'Standard deviation of block rate: {np.sqrt(var_blocked)}\n')

    ######### Check correctness of vectorised op #########
    # test_var = 0
    # for x in dropped_arr:
    #     test_var += (x - mean_dropped) ** 2

    # test_var /= (len(dropped_arr)-1)

    # print(test_var)
    ######################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process simulation args')
    parser.add_argument('--reps', default=10, type=int, help='Number of repitions of simulation runs (n) in lectures')
    parser.add_argument('--num_reserve', default=0, type=int, help='Number of reserve channels')
    args = parser.parse_args()

    analyse(args)