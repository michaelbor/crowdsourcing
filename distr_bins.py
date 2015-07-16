import numpy as np


class distr_bins:

	def __init__(self,num_of_bins, max_num):
		self.bins = [0]*num_of_bins
		self.bin_range = np.ceil(max_num/num_of_bins)
		self.max_num = max_num
		
	def insert(self, val):
		if val <= self.max_num and val >= 0:
			index = int(np.floor(val/self.bin_range))
			self.bins[index] += 1
		else:
			self.bins[-1] += 1
			
	def write_to_file(self,filename):
		x_coord = range(0+int(self.bin_range/2), self.max_num+int(self.bin_range/2), self.max_num/len(self.bins))
		total = [a*b for a,b in zip(x_coord, self.bins)]
		print [len(x_coord),len(self.bins)]
		print filename+' average: '+str(sum(total)/sum(self.bins))+' writing distribution to file. '+str([sum(total),sum(self.bins)])
		thefile = open(filename , 'w')
		for bin in self.bins:
			thefile.write("%s\n" %(bin))
			
		thefile.close()
		