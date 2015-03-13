#from events_handlers import *
#import utility_functions as utils


class Worker:
	""" Class that represents any step """

	def __init__(self, id, skills, avail_time):

		self.id = id
		self.skills = skills
		self.avail_time = avail_time
		self.used_time = 0
		
        
	def print_worker(self):
		return "(" + str(self.id) + "," +str(self.skills)+","\
		+str(self.avail_time)+")"
        
    
		
		
		

