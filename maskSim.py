import random as r
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np     
import matplotlib.cm as cm

# Set up population
popsize = 50
pop = np.zeros(popsize, dtype=[('pos', float, 2), ('mom', float, 2), ('clr', float, 1)])
pop['pos'] =  np.random.uniform(-1, 1, (popsize, 2))
pop['mom'] =  np.random.uniform(-1, 1, (popsize, 2))

pop[0]['clr'] = 1

# Set up figure
fig =  plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])

# Plot population on figure
scat = plt.scatter(pop['pos'][0], pop['pos'][1])
scat.set_array(pop['clr'])
scat.set_cmap('coolwarm')
scat.set_alpha(0.8)

# Frame update function
def _update_plot(i, fig, scat):
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
    scat.set_offsets(pop['pos'])
    return scat   

# Animate
anim = animation.FuncAnimation(fig, _update_plot, fargs = (fig, scat), frames = 100, interval = 100)          
plt.show()
