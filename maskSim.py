import random as r
from math import sqrt, e
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors as clr
import matplotlib.cm as cm

# Drifts momentum randomly, updates position based on momentum and more drift
def change_pos(avoidance=True):
    drift = 0.02
    check_radius = 0.1
    pythagorean = lambda x, y: sqrt((x ** 2) + (y ** 2))
    point = lambda x1, x2: abs(x1 - x2)  # difference between x vector components
    dist = lambda x1, x2: pythagorean(point(x1['pos'][0], x2['pos'][0]), point(x1['pos'][1], x2['pos'][1]))
    avoid_threshold = 0.5
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
        if len(list(nearby_inds)) and avoidance:
            risk_aversion = 3  # must be between 1 and 2.1
            total_mom_x = 0
            total_mom_y = 0
            for ind0 in nearby_inds:
                if ind0['clr'] >= avoid_threshold:
                    total_mom_x += ind0['mom'][0]
                    total_mom_y += ind0['mom'][1]
            try:
                if total_mom_y or total_mom_x:
                    ind['mom'][0] = total_mom_x / pythagorean(total_mom_x, total_mom_y)
                    ind['mom'][1] = total_mom_y / pythagorean(total_mom_x, total_mom_y)
            except ZeroDivisionError:
                pass
            ind['pos'][0] += risk_aversion * drift * ind['mom'][0]
            ind['pos'][1] += risk_aversion * drift * ind['mom'][1]
        else:
            ind['pos'][0] += drift * ind['mom'][0] + r.uniform(-drift, drift)
            ind['pos'][1] += drift * ind['mom'][1] + r.uniform(-drift, drift)
    scat.set_offsets(pop['pos'])

# Change color test
def change_clr(idx):
    trigger_radius = 0.05
    incubation_time = 5
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
                        ind2['clr'] += (1 - ind2['clr']) * ind1['clr']
                        NO_INT_FLAG = False

        if NO_INT_FLAG:
            ind1['clr'] *= falloff_rate

    scat.set_array(pop['clr'])

def change_hist():
    ax2.cla()
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, popsize])
    ax2.hist(pop['clr'], bins=np.arange(0,1,0.05))
    plt.draw()

# Function to run between each frame
def _update_plot(i, fig, scatter):
    change_pos(avoidance=False)
    change_clr(i)
    change_hist()
    return

# Set up population
popsize = 50
pop = np.zeros(popsize, dtype=[('pos', float, 2), ('mom', float, 2), ('clr', float, 1)])
pop['pos'] = np.random.uniform(-1, 1, (popsize, 2))
pop['mom'] = np.random.uniform(-1, 1, (popsize, 2))
pop['clr'] = np.random.uniform(0.03, 0.05, popsize)

# Set up figures
fig = plt.figure()
ax = fig.add_subplot(121)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax2 = fig.add_subplot(122)
ax2.set_xlim([0, 1])
ax2.set_ylim([0, popsize])

# Initial arena plot
scat = ax.scatter(pop['pos'][0], pop['pos'][1])
scat.set_array(pop['clr'])
scat.set_cmap('coolwarm')
scat.set_alpha(0.8)

# Initial histogram
hist = ax2.hist(pop['clr'], bins=np.arange(0,1,0.05))

# Animate
anim = animation.FuncAnimation(fig,
                               _update_plot,
                               fargs=(fig, scat),
                               frames=100,
                               interval=40)

plt.show()
