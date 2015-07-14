import math

class distr_bins:

	def __init__(self,num_of_bins, max_num):
		self.bins = [0]*num_of_bins
		self.bin_range = math.ceil(max_num/num_of_bins)
		self.max_num = max_num
		
	def insert(self, val):
		if val <= self.max_num:
			index = int(math.floor(val/self.bin_range))
			self.bins[index] += 1
		else:
			self.bins[-1] += 1
			
	def write_to_file(self,filename):
		thefile = open(filename , 'w')
		for bin in self.bins:
			thefile.write("%s\n" %(bin))
			
		thefile.close()
		