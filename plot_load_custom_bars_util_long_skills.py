#!/usr/bin/env python

import numpy as np
import matplotlib
#matplotlib.use('PDF')
import matplotlib.pyplot as plt
import params

matplotlib.rcParams['xtick.labelsize'] = 14
matplotlib.rcParams['ytick.labelsize'] = 14

# matplotlib.rcParams['pdf.fonttype'] = 42
# matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True

fig = plt.figure()

ax1 = fig.add_subplot(111)

width = 0.2
#offset = width

ax1.set_title("Utilization, Synthetic data, long skills",**params.title_font)   
 
#ax1.set_xlabel('Load [tasks/hour]')
ax1.set_ylabel('Workers utilization [%]',**params.axis_font)

#machines_p = np.array([0.8,0.6,0.4])
#machines_t = np.array([1.4,1.2,1])
machines_p = np.array([0.4,0.6,0.8])
machines_t = np.array([1,1.2,1.4])

off4 = 2
off8 = 4
off12 = 6
ax1.set_xticks(np.array([off4,off8,off12])+5*width)
ax1.set_xticklabels(['20 [tasks/hour]','50 [tasks/hour]','80 [tasks/hour]'],**params.axis_font_x)
plt.xlim(xmin=(off4+0.2),xmax=(off12+1.8))
plt.ylim(ymax=90)
x_unique=np.array([0.1,0.5,1])

rects_p=[0] * 3
rects_t=[0] * 3


data1 = np.genfromtxt("res_workers_custom_algo_1_long_skills.txt", delimiter=',', usecols=(1,3,4,6,7), \
dtype = [('load','i8'),('filename','S150'),('tat','f8'),('backlog','f8'),('util','f8')])

data2 = np.genfromtxt("res_workers_custom_algo_2_long_skills.txt", delimiter=',', usecols=(1,3,4,6,7), \
dtype = [('load','i8'),('filename','S150'),('tat','f8'),('backlog','f8'),('util','f8')])

data3 = np.genfromtxt("res_workers_custom_algo_3_long_skills.txt", delimiter=',', usecols=(1,3,4,6,7), \
dtype = [('load','i8'),('filename','S150'),('tat','f8'),('backlog','f8'),('util','f8')])

#===================================

y_mean_500 = [0]*3
y_mean_700 = [0]*3

load = 20
y_mean_500[0] = np.mean((data1['util'][np.where((data1['load']==load) & \
(np.char.find(data1['filename'],'1200')>-1))]))
y_mean_500[1] = np.mean((data2['util'][np.where((data2['load']==load) & \
(np.char.find(data2['filename'],'1200')>-1))]))
y_mean_500[2] = np.mean((data3['util'][np.where((data3['load']==load) & \
(np.char.find(data3['filename'],'1200')>-1))]))
y_mean_700[0] = np.mean((data1['util'][np.where((data1['load']==load) & \
(np.char.find(data1['filename'],'1600')>-1))]))
y_mean_700[1] = np.mean((data2['util'][np.where((data2['load']==load) & \
(np.char.find(data2['filename'],'1600')>-1))]))
y_mean_700[2] = np.mean((data3['util'][np.where((data3['load']==load) & \
(np.char.find(data3['filename'],'1600')>-1))]))


patterns=[3*'//',3*'o',3*'x']
colors = ['lightyellow','lightgreen','lavender'];
for i in range(len(patterns)):
	rects_p[i] = ax1.bar(machines_p[i]+off4, y_mean_500[i], width, color=colors[i],hatch=patterns[i],linewidth=2)

patterns=[4*'-',3*'\\\\',3*'\\']
colors = ['lightcoral','wheat','lightblue']
for i in range(len(patterns)):
	rects_t[i] = ax1.bar(machines_t[i]+off4, y_mean_700[i], width, color=colors[i],hatch=patterns[i],linewidth=2)

#===================================

y_mean_500 = [0]*3
y_mean_700 = [0]*3

load = 50
y_mean_500[0] = np.mean((data1['util'][np.where((data1['load']==load) & \
(np.char.find(data1['filename'],'1200')>-1))]))
y_mean_500[1] = np.mean((data2['util'][np.where((data2['load']==load) & \
(np.char.find(data2['filename'],'1200')>-1))]))
y_mean_500[2] = np.mean((data3['util'][np.where((data3['load']==load) & \
(np.char.find(data3['filename'],'1200')>-1))]))
y_mean_700[0] = np.mean((data1['util'][np.where((data1['load']==load) & \
(np.char.find(data1['filename'],'1600')>-1))]))
y_mean_700[1] = np.mean((data2['util'][np.where((data2['load']==load) & \
(np.char.find(data2['filename'],'1600')>-1))]))
y_mean_700[2] = np.mean((data3['util'][np.where((data3['load']==load) & \
(np.char.find(data3['filename'],'1600')>-1))]))

#print y_mean_500
#print y_mean_700

patterns=[3*'//',3*'o',3*'x']
colors = ['lightyellow','lightgreen','lavender'];
for i in range(len(patterns)):
	rects_p[i] = ax1.bar(machines_p[i]+off8, y_mean_500[i], width, color=colors[i],hatch=patterns[i],linewidth=2)

patterns=[4*'-',3*'\\\\',3*'\\']
colors = ['lightcoral','wheat','lightblue']
for i in range(len(patterns)):
	rects_t[i] = ax1.bar(machines_t[i]+off8, y_mean_700[i], width, color=colors[i],hatch=patterns[i],linewidth=2)

#ax1.bar(machines_p[2]+off8-0.01, y_mean_500[2]+1, width*1.2, color='w',hatch=patterns[i],linewidth=2, edgecolor='w',bottom=500)
#ax1.text(machines_p[2]+off8+0.1, 515, '1145', ha='center', va='bottom', fontsize=14)


print y_mean_500
print y_mean_700
#===================================

y_mean_500 = [0]*3
y_mean_700 = [0]*3

load = 80
y_mean_500[0] = np.mean((data1['util'][np.where((data1['load']==load) & \
(np.char.find(data1['filename'],'1200')>-1))]))
y_mean_500[1] = np.mean((data2['util'][np.where((data2['load']==load) & \
(np.char.find(data2['filename'],'1200')>-1))]))
y_mean_500[2] = np.mean((data3['util'][np.where((data3['load']==load) & \
(np.char.find(data3['filename'],'1200')>-1))]))
y_mean_700[0] = np.mean((data1['util'][np.where((data1['load']==load) & \
(np.char.find(data1['filename'],'1600')>-1))]))
y_mean_700[1] = np.mean((data2['util'][np.where((data2['load']==load) & \
(np.char.find(data2['filename'],'1600')>-1))]))
y_mean_700[2] = np.mean((data3['util'][np.where((data3['load']==load) & \
(np.char.find(data3['filename'],'1600')>-1))]))

patterns=[3*'//',3*'o',3*'x']
colors = ['lightyellow','lightgreen','lavender'];
for i in range(len(patterns)):
	rects_p[i] = ax1.bar(machines_p[i]+off12, y_mean_500[i], width, color=colors[i],hatch=patterns[i],linewidth=2)

patterns=[4*'-',3*'\\\\',3*'\\']
colors = ['lightcoral','wheat','lightblue']
for i in range(len(patterns)):
	rects_t[i] = ax1.bar(machines_t[i]+off12, y_mean_700[i], width, color=colors[i],hatch=patterns[i],linewidth=2)

#ax1.bar(machines_p[2]+off12-0.01, y_mean_500[2]+1, width*1.2, color='w',hatch=patterns[i],linewidth=2, edgecolor='w',bottom=750)
#ax1.text(machines_p[2]+off12+0.1, 765, '6862', ha='center', va='bottom', fontsize=14)

#ax1.bar(machines_t[2]+off12-0.01, y_mean_700[2]+1, width*1.2, color='w',hatch=patterns[i],linewidth=2, edgecolor='w',bottom=700)
#ax1.text(machines_t[2]+off12+0.1, 715, '2977', ha='center', va='bottom', fontsize=14)

#==========================================

print y_mean_500
print y_mean_700

#leg = ax1.legend()

#ax1.legend( (rects_p[0][0], rects_p[1][0], rects_p[2][0],rects_t[0][0], rects_t[1][0], rects_t[2][0] ), ('algo 1, 1200 w','algo 2, 1200 w','algo 3, 1200 w','algo 1, 1600 w','algo 2, 1600 w','algo 3, 1600 w'),bbox_to_anchor=(0, 0.9, 1,0.1), loc='upper left',
#           ncol=3,mode="expand",borderaxespad=0.,prop={'size': '13'})
ax1.legend( (rects_p[0][0], rects_p[1][0], rects_p[2][0],rects_t[0][0], rects_t[1][0], rects_t[2][0] ), (params.algo1+', 500 w',params.algo2+', 500 w',params.algo3+', 500 w',params.algo1+', 700 w',params.algo2+', 700 w',params.algo3+', 700 w'),bbox_to_anchor=(0, 0.9, 1,0.1), loc='upper left',
           ncol=3,mode="expand",borderaxespad=0.,prop={'size': '13'})


plt.tight_layout()
plt.savefig('load_custom_bars_util_long_skills.pdf', format='pdf')

plt.show()


