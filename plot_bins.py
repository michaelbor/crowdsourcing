#!/usr/bin/env python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import params
import sys

fig = plt.figure()

ax1 = fig.add_subplot(221)
n = 50
m = 8E4
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
data = np.genfromtxt(sys.argv[1], names=['x1'])
data1 = [sum(data['x1'][i:i + n]) for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax1.set_title("TAT distribution - Samasource, All")    
ax1.set_xlabel('TAT [sec]')
ax1.set_ylabel('Number of tasks')
ax1.bar(x_coord1[0:lim], data1[0:lim], width = params.bins_max_val/(params.bins_num_of_bins/n))


ax2 = fig.add_subplot(222)
n = 50
m = 8E4
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
data = np.genfromtxt(sys.argv[2], names=['x1'])
data1 = [sum(data['x1'][i:i + n]) for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax2.set_title("TAT distribution - Samasource, Realtime")    
ax2.set_xlabel('TAT [sec]')
ax2.set_ylabel('Number of tasks')
ax2.bar(x_coord1[0:lim], data1[0:lim], width = params.bins_max_val/(params.bins_num_of_bins/n))


ax3 = fig.add_subplot(223)
n = 50
m = 8E4
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
data = np.genfromtxt(sys.argv[3], names=['x1'])
data1 = [sum(data['x1'][i:i + n]) for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax3.set_title("TAT distribution - Our Algo, All")    
ax3.set_xlabel('TAT [sec]')
ax3.set_ylabel('Number of tasks')
ax3.bar(x_coord1[0:lim], data1[0:lim], width = params.bins_max_val/(params.bins_num_of_bins/n))


ax4 = fig.add_subplot(224)
m = 8E4
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
data = np.genfromtxt(sys.argv[4], names=['x1'])
data1 = [sum(data['x1'][i:i + n]) for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax4.set_title("TAT distribution - Our Algo, Realtime")    
ax4.set_xlabel('TAT [sec]')
ax4.set_ylabel('Number of tasks')
ax4.bar(x_coord1[0:lim], data1[0:lim], width = params.bins_max_val/(params.bins_num_of_bins/n))


plt.savefig('bins.pdf', format='pdf')

plt.show()


