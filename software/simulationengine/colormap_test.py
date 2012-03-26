import os,sys,math,random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import gtk

import reactor



temp_slices = [[[0.0 for z in range(reactor.default_depth)] for x in range(len(reactor.default_layout))] for y in range(len(reactor.default_layout[0]))]
neutron_slices = [[[0.0 for z in range(reactor.default_depth)] for x in range(len(reactor.default_layout))] for y in range(len(reactor.default_layout[0]))]
#temp_slices = [[[128.0 for z in range(reactor.default_depth)] for x in range(len(reactor.default_layout)+1)] for y in range(len(reactor.default_layout[0])+1)]
#neutron_slices = [[[128.0 for z in range(reactor.default_depth)] for x in range(len(reactor.default_layout)+1)] for y in range(len(reactor.default_layout[0])+1)]

# Fill with random data
for z in range(len(temp_slices)):
    for x in range(len(temp_slices[z])):
        for y in range(len(temp_slices[z][x])):
            if reactor.default_layout[x][y] == ' ':
                continue
            temp_slices[z][x][y] = random.random() * 1000

all_slices_max = max(max(max(temp_slices)))


# These need to be one larger than the actual data
x = np.arange(len(reactor.default_layout)+1) 
y = np.arange(len(reactor.default_layout[0])+1) 
X, Y = np.meshgrid(x,y)

# figure dimensions
cols = 2
rows = int(math.ceil(float(len(temp_slices))/cols))


# Create the subplots
fig, axes = plt.subplots(rows, cols)

#print axes

# Normalize the heatmap
temp_norm = mpl.colors.Normalize(0.0, all_slices_max)

for i in range(len(temp_slices)):
    row = i % rows
    col = (i/rows) % cols
    axes[row][col].pcolor(X,Y,temp_slices[i], norm=temp_norm)
    axes[row][col].set_title("Slice %d" % i)

CB1 = mpl.colorbar.ColorbarBase(axes[rows-1][cols-1], norm=temp_norm, orientation='horizontal')
CB1.set_label('Temperature')



plt.show()