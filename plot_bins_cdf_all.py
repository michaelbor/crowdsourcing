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

ax1 = fig.add_subplot(111)

n = 50
m = 2E5
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
plt.ylim([0.5,1.2])
data = np.genfromtxt("res1/bins_sama.txt", names=['x1'])
total = float(sum(data['x1']))
data1 = [sum(data['x1'][i:i + n])/total for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
ax1.set_title("TAT CDF - All projects",**params.title_font)    
ax1.set_xlabel('TAT [sec]',**params.axis_font_x)
ax1.set_ylabel('Fraction of tasks',**params.axis_font)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
acc = 0
data_cdf = [0]*len(data1[0:lim])
for i in range(0,len(data1[0:lim])):
	acc += data1[i]
	data_cdf[i] = acc

#ax1.plot(x_coord1[0:lim], data1[0:lim])
ax1.plot(x_coord1[0:lim], data_cdf, linewidth = 2, marker='v', color='red',label='sama, all')


avg = sum([a*b for a,b in zip(x_coord,data['x1'])])/total
print avg
ax1.axvline(avg,0,0.3,linewidth=2, color='r')



n = 50
m = 2E5
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
data = np.genfromtxt("res1/bins_our_algo.txt", names=['x1'])
total = float(sum(data['x1']))
data1 = [sum(data['x1'][i:i + n])/total for i in range(0, len(data['x1']), n)]
x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))

acc = 0
data_cdf = [0]*len(data1[0:lim])
for i in range(0,len(data1[0:lim])):
	acc += data1[i]
	data_cdf[i] = acc
	
ax1.plot(x_coord1[0:lim], data_cdf,linewidth = 2, marker='o', color='green', label='our, all')

avg = sum([a*b for a,b in zip(x_coord,data['x1'])])/total
print avg
ax1.axvline(avg,0,0.3,linewidth=2, color='g')



ax1.legend()

plt.tight_layout()



plt.savefig('bins_cdf_all.pdf', format='pdf')

plt.show()


