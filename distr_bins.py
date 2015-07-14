

class distr_bins:

	def __init__(self,num_of_bins, max_num):
		bins = [0]*num_of_bins
		bin_range = ceil(max_num/num_of_bins)
		
	def insert(self, val):
		if val <= max_num:
			index = floor(val/bin_range)
			bins[index] += 1