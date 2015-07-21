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

x_coord = range(400,1600,50)

ax1 = fig.add_subplot(111)

#plt.xlim([0,m])
#plt.ylim([0.5,1.2])
data = np.genfromtxt("workers_res1.txt", delimiter=',', usecols=(2,12), \
dtype = [('filename','S150'),('backlog','f8')])


backlog_means = []
for x in x_coord:
	tmp = '_'+str(x)+'.txt'
	backlog_means.append(np.mean(data['backlog'][np.where(np.char.find(data['filename'],tmp)>-1)]))
	
	
#print all_tat_means
#print rt_tat_means


ax1.set_title("Backlog, Samasource data, Real timezones (-4,0,3,5)",**params.title_font)    
ax1.set_xlabel('Num of workers',**params.axis_font_x)
ax1.set_ylabel('Average backlog [number of unscheduled steps]',**params.axis_font)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

ax1.plot(x_coord, backlog_means, linewidth = 2, marker='v', color='red',label='all projects')
#ax1.plot(x_coord, rt_tat_means, linewidth = 2, marker='o', color='green',label='rt projects')

#ax1.legend()

plt.tight_layout()



plt.savefig('workers_tat_backlog.pdf', format='pdf')

plt.show()


