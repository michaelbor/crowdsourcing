#!/usr/bin/env python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import params
import sys

matplotlib.rcParams['xtick.labelsize'] = 11
matplotlib.rcParams['ytick.labelsize'] = 11

fig = plt.figure()
plt.subplots_adjust(hspace = 0.5, wspace = 0.3)

x_coord = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins))
bin_range = np.ceil(params.bins_max_val/params.bins_num_of_bins)
x_coord = range(0+int(bin_range/2), params.bins_max_val+int(bin_range/2), int(bin_range))



ax2 = fig.add_subplot(111)
n = 50
#m = 4E5
m = 2.6E5
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
plt.xlim([0,m])
plt.ylim([0.1,1.02])
data = np.genfromtxt("res_sama_625_workers_3_days_tat/bins_sama.txt", names=['x1'])
total = float(sum(data['x1']))
data1 = [sum(data['x1'][i:i + n])/total for i in range(0, len(data['x1']), n)]
x_coord1 = range(0+int(bin_range/2)*n,params.bins_max_val+int(bin_range/2)*n,params.bins_max_val/(params.bins_num_of_bins/n))
ax2.set_title("TAT CDF, Samsource data, All projects",**params.title_font)    
ax2.set_xlabel('TAT [sec]',**params.axis_font_x)
ax2.set_ylabel('Fraction of tasks',**params.axis_font)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
acc = 0
data_cdf = [0]*len(data1[0:lim])
for i in range(0,len(data1[0:lim])):
	acc += data1[i]
	data_cdf[i] = acc

avg = sum([a*b for a,b in zip(x_coord,data['x1'])])/total
print avg
print x_coord1[0]
ax2.plot(x_coord1[0:lim], data_cdf, linewidth = 2, marker='v', color='red',label='Algo: Sama, avg=%.1e'%round(avg))
#ax2.axvline(avg,0,0.3,linewidth=2, color='r')




#ax4 = fig.add_subplot(224)
#m = 8E4
lim = int(m/(params.bins_max_val/(params.bins_num_of_bins/n)))
data = np.genfromtxt("res_sama_625_workers_3_days_tat/bins_our_algo.txt", names=['x1'])
total = float(sum(data['x1']))
data1 = [sum(data['x1'][i:i + n])/total for i in range(0, len(data['x1']), n)]
#x_coord1 = range(0,params.bins_max_val,params.bins_max_val/(params.bins_num_of_bins/n))
#ax4.set_title("TAT distribution - Our Algo, Realtime",**params.title_font)    
#ax4.set_xlabel('TAT [sec]',**params.axis_font_x)
#ax4.set_ylabel('Fraction of tasks',**params.axis_font)
#ax4.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
acc = 0
data_cdf = [0]*len(data1[0:lim])
for i in range(0,len(data1[0:lim])):
	acc += data1[i]
	data_cdf[i] = acc
	
avg = sum([a*b for a,b in zip(x_coord,data['x1'])])/total
print avg
ax2.plot(x_coord1[0:lim], data_cdf, linewidth = 2, marker='o', color='green',label='Algo: 1, avg=%.1e'% round(avg))
#ax2.axvline(avg,0,0.3,linewidth=2, color='g')



ax2.legend(loc='center right')

plt.tight_layout()



plt.savefig('bins_cdf_all_3_days_tat.pdf', format='pdf')

plt.show()


