import random as r
from math import sqrt, e
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors as clr
import matplotlib.cm as cm

# Drifts momentum randomly, updates position based on momentum and more drift
def change_pos():
    drift = 0.01
    for ind in pop:
        ind['mom'][0] += r.uniform(-drift, drift)
        ind['mom'][1] += r.uniform(-drift, drift)
        if ind['pos'][0] > 1:
            ind['mom'][0] = -abs(ind['mom'][0])
        if ind['pos'][0] < -1:
            ind['mom'][0] = abs(ind['mom'][0])
        if ind['pos'][1] > 1:
            ind['mom'][1] = -abs(ind['mom'][1])
        if ind['pos'][1] < -1:
            ind['mom'][1] = abs(ind['mom'][1])
        ind['pos'][0] += drift * ind['mom'][0] + r.uniform(-drift, drift)
        ind['pos'][1] += drift * ind['mom'][1] + r.uniform(-drift, drift)
    scat.set_offsets(pop['pos'])

# Change color test
def change_clr(idx):
    trigger_radius = 0.06
    incubation_time = 10
    falloff_rate = (incubation_time-1)/incubation_time
    euclidean_dist = lambda x, y: sqrt((x**2) + (y**2))
    point = lambda x1, x2: abs(x1 - x2)  # difference between x vector components
    for ind1 in pop:
        NO_INT_FLAG = True  # interaction flag
        for ind2 in pop:
                if ind1 != ind2:
                    if euclidean_dist(point(ind1['pos'][0], ind2['pos'][0]),
                                      point(ind1['pos'][1], ind2['pos'][1])) <= trigger_radius:
                        ind1['clr'] += (1 - ind1['clr']) * ind2['clr']
                        pop[0]['clr'] = 1  # eternal source
                        ind2['clr'] += (1 - ind2['clr']) * ind1['clr']
                        pop[0]['clr'] = 1  # eternal source
                        NO_INT_FLAG = False

        if NO_INT_FLAG:
            ind1['clr'] *= falloff_rate
            pop[0]['clr'] = 1  # eternal source

    scat.set_array(pop['clr'])

# Function to run between each frame
def _update_plot(i, fig, scatter):
    change_pos()
    change_clr(i)
    return scat

# Set up population
popsize = 50
pop = np.zeros(popsize, dtype=[('pos', float, 2), ('mom', float, 2), ('clr', float, 1)])
pop['pos'] = np.random.uniform(-1, 1, (popsize, 2))
pop['mom'] = np.random.uniform(-1, 1, (popsize, 2))

# Patient zero
pop[0]['clr'] = 1

# Set up figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])

# Initial plot
scat = plt.scatter(pop['pos'][0], pop['pos'][1])
scat.set_array(pop['clr'])
scat.set_cmap('coolwarm')
scat.set_alpha(0.8)

# Animate
anim = animation.FuncAnimation(fig,
                               _update_plot,
                               fargs=(fig, scat),
                               frames=100,
                               interval=20)

plt.show()
