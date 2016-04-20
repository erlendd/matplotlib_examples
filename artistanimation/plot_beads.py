import matplotlib
matplotlib.use('Agg')
import seaborn as sns; sns.set()
import matplotlib.animation as animation
from matplotlib import gridspec
import pandas as pd
import numpy as np
import os.path

sns.set_context('talk')

Ts = []
fns = []
for T in range(200, 25, -5):
    fn = 'T{}/eck.out'.format(T)
    if os.path.isfile(fn):
        Ts.append(T)
        fns.append( fn )

#fig = sns.plt.figure()
#
fig = sns.plt.figure(figsize=(10, 6.5))
gs = gridspec.GridSpec(1,2, width_ratios=[12, 1])
ax1 = sns.plt.subplot( gs[0] )
ax2 = sns.plt.subplot( gs[1] )

ax2.yaxis.set_label_position('right')
ax2.yaxis.tick_right()
ax2.set_xticks([], minor=False)
ax2.grid(b=False)

ax1.set_xlabel(ur'Reaction coordinate (H displacement in \u00c5)')
ax1.set_ylabel('Transition barrier (eV)')
ax2.set_ylabel('Temperature (K)')

ax1.set_xlim( [0, 1.40] )
ax1.set_ylim( [0, 0.35] )

poten = pd.read_table('../1_potplot/energy.dat', delim_whitespace=True)
poten[[0]] = poten[[0]].values + 0.11
poten[[1]] = poten[[1]].values + 0.018
potential_plot, = ax1.plot( poten[[0]], poten[[1]], c='g', linewidth=3, alpha=0.5 )

ims = []
for idx, fn in enumerate(fns):
    df = pd.read_table(fn, skiprows=1, delim_whitespace=True)
    df = df[100:]
    df[[1]] = df[[1]].values + 2.8 + 0.31
    df[[2]] = df[[2]].values + 0.02
    T = Ts[idx]
    x_centroid = df[[1]].mean()
    E_centroid = df[[2]].mean()

    temperature_plot, = ax2.bar(0, T, color='pink')

    # must only have one label for each 'type' here...
    centroid_label = None
    beads_label = None
    if idx == 0:
        centroid_label = 'centroid'
	beads_label = 'beads'

    ims.append( [potential_plot,
                 ax1.scatter( df[[1]], df[[2]], s=100, alpha=0.7, label=beads_label ), 
                 ax1.scatter( x_centroid, E_centroid, c='r', s=200, label=centroid_label ),
		 ax1.annotate('T = {}K'.format(T), (0.1, 0.3), size=18),
		 temperature_plot] 
	      )
    ax1.legend()


im_ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True)

sns.plt.tight_layout()
im_ani.save('hqtst_beads_anim.mp4')

#sns.plt.savefig('out.png')

