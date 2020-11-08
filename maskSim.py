import random as r
from math import sqrt
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors as clr
import matplotlib.cm as cm

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

def change_clr():
    trigger_radius = 0.06
    risk_num = 0.5
    euclidean_dist = lambda x, y: sqrt((x**2) + (y**2))
    point = lambda x1, x2: abs(x1 - x2)
    for ind1 in pop:
        for ind2 in pop:
            if euclidean_dist(point(ind1['pos'][0], ind2['pos'][1]),
                              point(ind2['pos'][0], ind2['pos'][1])) <= trigger_radius:
                ind1['clr'] += risk_num
                ind2['clr'] += risk_num

def _update_plot(i, fig, scatter):
    change_pos()  # updates positions
    change_clr()
    scat.set_offsets(pop['pos'])
    return scat


# Set up population
popsize = 50
pop = np.zeros(popsize, dtype=[('pos', float, 2), ('mom', float, 2), ('clr', float, 1)])
pop['pos'] = np.random.uniform(-1, 1, (popsize, 2))
pop['mom'] = np.random.uniform(-1, 1, (popsize, 2))

pop[0]['clr'] = 1

# Set up figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])

# Plot population on figure
scat = plt.scatter(pop['pos'][0], pop['pos'][1])
scat.set_array(pop['clr'])
scat.set_cmap('coolwarm')
scat.set_alpha(0.8)

anim = animation.FuncAnimation(fig, _update_plot,
                               fargs=(fig, scat),
                               frames=100,
                               interval=100)

# Animate
anim = animation.FuncAnimation(fig, _update_plot, fargs = (fig, scat), frames = 100, interval = 100)
plt.show()
