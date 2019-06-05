import numpy as np
import random
import copy
import multiprocessing
from multiprocessing import Pool
import time


def M_T(input_config, Temperature):
    Spin_config = copy.deepcopy(input_config)
    step = 0
    Net_spin = [np.sum(Spin_config)]
    while step <= 1000000:
        site_a = np.round(random.random() * (N-1)); site_b = np.round(random.random() * (N-1))
        site_a = np.int_(site_a); site_b = np.int_(site_b)
        site_a_minus1 = site_a - 1; site_a_plus1 = site_a + 1
        site_b_minus1 = site_b - 1; site_b_plus1 = site_b + 1
        # Here is the boundary condition
        if site_a == 0:
            site_a_minus1 = (N-1)
        if site_a == (N-1):
            site_a_plus1 = 0
        if site_b == 0:
            site_b_minus1 = (N-1)
        if site_b == (N-1):
            site_b_plus1 = 0
        beta_deltaE = - 2 * (1. / Temperature) * (-Spin_config[site_a, site_b]) * (
            Spin_config[site_a, site_b] + Spin_config[site_a_minus1, site_b] +
            Spin_config[site_a_plus1, site_b_minus1]+ Spin_config[site_a, site_b_plus1])
        if beta_deltaE <= 0:
            prob = 1
            Spin_config[site_a, site_b] = (-Spin_config[site_a, site_b])
        else:
            prob = np.exp(-beta_deltaE)
            random_x = random.random()
            if prob >= random_x:
                Spin_config[site_a, site_b] = (-Spin_config[site_a, site_b])
            else:
                pass
        Net_spin.append(np.sum(Spin_config))
        step += 1
    return Net_spin, Spin_config


def main(seed=None):
    np.random.seed(seed)
    init_config = np.round(np.random.rand(N, N))
    init_config = (init_config-0.5)*2
    init_config = np.int_(init_config)
    net_spin_i = np.average(M_T(init_config, i)[0])
    return net_spin_i


start_time = time.time()
net_spin = []
N = 20
for i in np.arange(1, 10, 1):
    net_spin_j = []
    cores = multiprocessing.cpu_count()
    print(cores)
    pool = Pool(processes=cores)
    for net_spin_i in pool.imap(main, range(1000)):
        net_spin_j.append(np.abs(net_spin_i))
    net_spin.append(np.average(net_spin_j))
print('total time cost', time.time()-start_time)
np.save('netspin.npy', net_spin)

