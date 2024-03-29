#!/usr/bin/env python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import params
import sys

matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8


fig = plt.figure()
plt.subplots_adjust(hspace = 0.5, wspace = 0.3)

x_coord = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins))

ax1 = fig.add_subplot(221)

n = 50
m = 2E5
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
plt.ylim([0,1])
data = np.genfromtxt(sys.argv[1], names=['x1'])
total = float(sum(data['x1']))
data1 = [sum(data['x1'][i:i + n])/total for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax1.set_title("TAT distribution - Samasource, All",**params.title_font)    
ax1.set_xlabel('TAT [sec]',**params.axis_font_x)
ax1.set_ylabel('Fraction of tasks',**params.axis_font)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax1.bar(x_coord1[0:lim], data1[0:lim], width = params.bins_max_val/(params.bins_num_of_bins/n))

avg = sum([a*b for a,b in zip(x_coord,data['x1'])])/total
print avg
ax1.axvline(avg,0,0.5,linewidth=4, color='r')

ax2 = fig.add_subplot(222)
n = 50
m = 8E4
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
plt.ylim([0,1])
data = np.genfromtxt(sys.argv[2], names=['x1'])
total = float(sum(data['x1']))
data1 = [sum(data['x1'][i:i + n])/total for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax2.set_title("TAT distribution - Samasource, Realtime",**params.title_font)    
ax2.set_xlabel('TAT [sec]',**params.axis_font_x)
ax2.set_ylabel('Fraction of tasks',**params.axis_font)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax2.bar(x_coord1[0:lim], data1[0:lim], width = params.bins_max_val/(params.bins_num_of_bins/n))

avg = sum([a*b for a,b in zip(x_coord,data['x1'])])/total
print avg
ax2.axvline(avg,0,0.5,linewidth=4, color='r')


ax3 = fig.add_subplot(223)
n = 50
m = 8E4
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
plt.ylim([0,1])
data = np.genfromtxt(sys.argv[3], names=['x1'])
total = float(sum(data['x1']))
data1 = [sum(data['x1'][i:i + n])/total for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax3.set_title("TAT distribution - Our Algo, All",**params.title_font)    
ax3.set_xlabel('TAT [sec]',**params.axis_font_x)
ax3.set_ylabel('Fraction of tasks',**params.axis_font)
ax3.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax3.bar(x_coord1[0:lim], data1[0:lim], width = params.bins_max_val/(params.bins_num_of_bins/n))

avg = sum([a*b for a,b in zip(x_coord,data['x1'])])/total
print avg
ax3.axvline(avg,0,0.5,linewidth=4, color='r')


ax4 = fig.add_subplot(224)
m = 8E4
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
plt.ylim([0,1])
data = np.genfromtxt(sys.argv[4], names=['x1'])
total = float(sum(data['x1']))
data1 = [sum(data['x1'][i:i + n])/total for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax4.set_title("TAT distribution - Our Algo, Realtime",**params.title_font)    
ax4.set_xlabel('TAT [sec]',**params.axis_font_x)
ax4.set_ylabel('Fraction of tasks',**params.axis_font)
ax4.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax4.bar(x_coord1[0:lim], data1[0:lim], width = params.bins_max_val/(params.bins_num_of_bins/n))

avg = sum([a*b for a,b in zip(x_coord,data['x1'])])/total
print avg
ax4.axvline(avg,0,0.5,linewidth=4, color='r')

plt.savefig('bins.pdf', format='pdf')

plt.show()


