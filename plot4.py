import numpy as np
import matplotlib
#matplotlib.use('PDF')
import matplotlib.pyplot as plt

data = np.genfromtxt('res.txt', names=['x1', 'x2', 'x3', 'x4', 'x5', 'x6'])


fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("max_skills = 5, max_skills_step = 3, max_skills_worker = 3, \n\
max_ordinal = 2, min_skill_time = 500, max_skill_time = 6000, time_step = 600s") 
ax1.set_xlabel('Tasks per hour')
ax1.set_ylabel('Avg backlog')

'''
x_unique = np.unique(data['x2'])
y_mean = np.zeros_like(x_unique)
y_std = np.zeros_like(x_unique)
k = 0
for i in x_unique:
	#print np.where(data['x2']==i)
	y_mean[k] = np.mean(data['x7'][np.where(data['x2']==i)])
	y_std[k] = np.std(data['x7'][np.where(data['x2']==i)])
	k = k+1

y_error = [y_std, y_std]
colors=['r','g','b','m','black']
ax1.set_color_cycle(colors)
'''

#ax1.scatter(data['x2'], data['x7'], label='Br1, 3 iter')
ax1.plot(data['x2'][np.where(data['x1']==3)], data['x4'][np.where(data['x1']==3)], label='Algo 3')
#ax1.plot(data['x2'][np.where(data['x1']==2)], data['x3'][np.where(data['x1']==2)], label='Algo 2')

#ax1.errorbar(1-x_unique, y_mean, y_error, fmt='-o', label='mean and std')


leg = ax1.legend()
plt.savefig('myplot4.pdf', format='pdf')

plt.show()


