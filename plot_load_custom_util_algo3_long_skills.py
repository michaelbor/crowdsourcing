#!/usr/bin/env python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import params
import sys

matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12

fig = plt.figure()
plt.subplots_adjust(hspace = 0.5, wspace = 0.3)

x_coord = range(10,90,10)

ax1 = fig.add_subplot(111)

plt.xlim([0,82])
#plt.ylim([0,1500])
data = np.genfromtxt("res_workers_custom_algo_3_long_skills.txt", delimiter=',', usecols=(1,3,4,6,7), \
dtype = [('load','i8'),('filename','S150'),('tat','f8'),('backlog','f8'),('util','f8')])


tat_means1 = []
tat_means2 = []
tat_means3 = []
for x in x_coord:
	tat_means1.append(np.mean(data['util'][np.where((np.char.find(data['filename'],'1200')>-1) \
	& (data['load']==x))]))
	tat_means2.append(np.mean(data['util'][np.where((np.char.find(data['filename'],'1400')>-1) \
	& (data['load']==x))]))
	tat_means3.append(np.mean(data['util'][np.where((np.char.find(data['filename'],'1600')>-1) \
	& (data['load']==x))]))


ax1.set_title("Utilization, Synthetic data, Max ordering = 3, Real timezones (-4,0,3,5), Algorithm 3",**params.title_font)    
ax1.set_xlabel('Tasks per hour',**params.axis_font_x)
ax1.set_ylabel('Workers utilization [%]',**params.axis_font)
#ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

ax1.plot(x_coord, tat_means1, linewidth = 2, marker='v', color='red',label='1200 workers')
ax1.plot(x_coord, tat_means2, linewidth = 2, marker='o', color='green',label='1400 workers')
ax1.plot(x_coord, tat_means3, linewidth = 2, marker='x', color='blue',label='1600 workers')


ax1.legend(loc='upper left')

plt.tight_layout()



plt.savefig('load_custom_util_algo3_long_skills.pdf', format='pdf')

plt.show()


