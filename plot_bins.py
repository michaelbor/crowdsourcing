import numpy as np
import matplotlib
#matplotlib.use('PDF')
import matplotlib.pyplot as plt

data = np.genfromtxt('bins.txt', names=['x1'])
x_coord = range(0,1000000,1000000/100)

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("TAT distribution")    
ax1.set_xlabel('TAT [sec]')
ax1.set_ylabel('Number of tasks')


ax1.bar(x_coord, data['x1'], label='Algo 1')


leg = ax1.legend()
plt.savefig('bins.pdf', format='pdf')

plt.show()


