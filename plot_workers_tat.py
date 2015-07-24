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

x_coord = range(400,1650,50)

ax1 = fig.add_subplot(111)

plt.xlim([350,1650])
#plt.ylim([0.5,1.2])
data = np.genfromtxt("workers_res1.txt", delimiter=',', usecols=(2,3,7), \
dtype = [('filename','S150'),('all_tat','f8'),('rt_tat','f8')])


all_tat_means = []
rt_tat_means = []
for x in x_coord:
	tmp = '_'+str(x)+'.txt'
	all_tat_means.append(np.mean(data['all_tat'][np.where(np.char.find(data['filename'],tmp)>-1)]))
	rt_tat_means.append(np.mean(data['rt_tat'][np.where(np.char.find(data['filename'],tmp)>-1)]))
	
#print all_tat_means
#print rt_tat_means


ax1.set_title("TAT, Samasource data, Real timezones (-4,0,3,5)",**params.title_font)    
ax1.set_xlabel('Num of workers',**params.axis_font_x)
ax1.set_ylabel('TAT [sec]',**params.axis_font)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

ax1.plot(x_coord, all_tat_means, linewidth = 2, marker='v', color='red',label='all projects')
ax1.plot(x_coord, rt_tat_means, linewidth = 2, marker='o', color='green',label='rt projects')

ax1.legend()

plt.tight_layout()



plt.savefig('workers_tat.pdf', format='pdf')

plt.show()


