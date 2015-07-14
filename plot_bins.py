#!/usr/bin/env python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import params
import sys

data = np.genfromtxt(sys.argv[1], names=['x1'])
x_coord = range(0,params.bins_max_val,params.bins_max_val/params.bins_num_of_bins)

n = 1000
data1 = [sum(data['x1'][i:i + n]) for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("TAT distribution")    
ax1.set_xlabel('TAT [sec]')
ax1.set_ylabel('Number of tasks')


#ax1.bar(x_coord, data['x1'], width = params.bins_max_val/params.bins_num_of_bins)
ax1.bar(x_coord1, data1, width = params.bins_max_val/(params.bins_num_of_bins/n))


#leg = ax1.legend()
plt.savefig('bins.pdf', format='pdf')

plt.show()


