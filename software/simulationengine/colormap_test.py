import os,sys,math,random
import numpy as np
import matplotlib.pyplot as plt

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

# These need to be one larger than the actual data
x = np.arange(len(reactor.default_layout)+1) 
y = np.arange(len(reactor.default_layout[0])+1) 

print x,y

X, Y = np.meshgrid(x,y)

rows = 4
cols = 2
#fig, axes = plt.subplots(len(temp_slices), 1, sharex=True, sharey=True)
fig, axes = plt.subplots(rows, cols, sharex=True, sharey=True)

print axes

for i in range(len(temp_slices)):
    row = i % rows
    col = (i/rows) % cols
    axes[row][col].pcolor(X,Y,temp_slices[i])




plt.show()