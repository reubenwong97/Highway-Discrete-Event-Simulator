import numpy as np
from scipy import stats

class Randoms(object):
    # NOTE: All distributions valid at critical value 0.05
    def __init__(self, seed):
        self.expon = stats.expon
        self.seed = seed
        np.random.seed(self.seed)
        # print(f"Rng created with seed: {seed}")

    def random_interarrival(self, beta=1.369817):
        # Verified
        # KstestResult(statistic=0.010015330445135917, pvalue=0.26664034156645433)
        params = (2.5090155759244226e-05, 1.3697918363207653)
        return self.expon.rvs(loc=params[0], scale=params[1])

        # Left here for completeness, but we will use scipy
        # u = np.random.uniform()
        # return -beta * np.log(1 - u)
    
    def random_direction(self):
        '''
        2-point distribution with probability 0.5 each
        '''
        if np.random.random() < 0.5:
            return -1
        else:
            return 1

    def random_position(self):
        '''
        Return uniform random number [0, 1] indicating relative position within a cell
        '''
        return np.random.uniform()

    def random_duration(self):
        # u = np.random.uniform()
        # return -beta * np.log(1 - u)

        # NOTE: our data starts from 12...-> not shifting the distribution fails the KStest
        # as there is a huge D due to the initial few numbers
        # we accumulate a huge amount of probability in the range 0 - 12, leading us to have a huge D
        # using scipy's module makes this  better, params[0] does this shifting
        # although the distributions end up looking very similar, this is used as it is more correct
        params = (10.003951603252272, 99.83194913549542)
        # Verified
        # KstestResult(statistic=0.005854123916584519, pvalue=0.8809285916372338)
        return self.expon.rvs(loc=params[0], scale=params[1])

    def random_speed(self, mu=0.033353, std=0.002505):
        return np.random.normal(mu, std)

    def random_station(self, low=0, high=20):
        '''
        Returns "Discrete Uniform" variate. Excludes high
        '''
        # Verified
        # Power_divergenceResult(statistic=25.656000000000002, pvalue=0.14006290765463547)
        # indexes 0 to 19 for our 20 stations
        return np.random.randint(low, high)