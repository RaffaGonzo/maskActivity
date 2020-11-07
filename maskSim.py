import random as r
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def _update_plot(i, fig, scatter):
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
        ind['pos'][0] += drift*ind['mom'][0] + r.uniform(-drift, drift)
        ind['pos'][1] += drift*ind['mom'][1] + r.uniform(-drift, drift)
    scatter.set_offsets(pop['pos'])
    return scatter        

popsize = 50
pop = np.zeros(popsize, dtype=[('pos', float, 2), ('mom', float, 2), ('col', float, 4)])
pop['pos'] =  np.random.uniform(-1, 1, (popsize, 2))
pop['mom'] =  np.random.uniform(-1, 1, (popsize, 2))


# Set up figure
fig =  plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])

scatter = plt.scatter(pop['pos'][0], pop['pos'][1], c = pop['col'])
scatter.set_alpha(0.8)

anim = animation.FuncAnimation(fig, _update_plot, fargs = (fig, scatter), frames = 100, interval = 100)          
plt.show()
 

