'''
Author: Raphael Gonzalez (RAffA)
'''
import random as r
from math import sqrt, e
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animations

def change_pos():
    drift = 0.02
    check_radius = 0.7
    euclidean_dist = lambda x, y: sqrt((x ** 2) + (y ** 2))
    point = lambda x1, x2: abs(x1 - x2)  # difference between x vector components
    dist = lambda x1, x2: euclidean_dist(point(x1['pos'][0], x2['pos'][0]), point(x1['pos'][1], x2['pos'][1]))
    for ind in pop:
        ind['mom'][0] += r.uniform(-drift, drift)
        ind['mom'][1] += r.uniform(-drift, drift)
        if ind['pos'][0] > 1:
            ind['mom'][0] = -abs(ind['mom'][0])
            ind['pos'][0] = 1
        elif ind['pos'][0] < -1:
            ind['mom'][0] = abs(ind['mom'][0])
            ind['pos'][0] = -1
        if ind['pos'][1] > 1:
            ind['mom'][1] = -abs(ind['mom'][1])
            ind['pos'][1] = 1
        elif ind['pos'][1] < -1:
            ind['mom'][1] = abs(ind['mom'][1])
            ind['pos'][1] = -1
        nearby_inds = filter(lambda x: dist(x, ind) <= check_radius and x != ind, pop)
        if len(list(nearby_inds)):
            total_mom_x = 0
            total_mom_y = 0
            for ind0 in nearby_inds:
                total_mom_x += ind0['mom'][0]
                total_mom_y += ind0['mom'][1]
            ind['mom'][0] = total_mom_x
            ind['mom'][1] = total_mom_y

        else:
            ind['pos'][0] += drift * ind['mom'][0] + r.uniform(-drift, drift)
            ind['pos'][1] += drift * ind['mom'][1] + r.uniform(-drift, drift)
    scat.set_offsets(pop['pos'])

popsize = 50
pop = np.zeros(popsize, dtype=[('pos', float, 2), ('mom', float, 2), ('clr', float, 1)])

scat = plt.scatter(pop['pos'][0], pop['pos'][1])
