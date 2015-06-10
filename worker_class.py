import utils
import stats
import params

class Worker:
	""" Class that represents a worker """

	def __init__(self, id, skills, avail_time_start, avail_time_end, timezone):

		self.id = id
		self.skills = skills
		self.avail_time_start = avail_time_start
		self.avail_time_end = avail_time_end
		self.avail_time = avail_time_end - avail_time_start
		self.timezone = timezone
		self.used_time = 0
		self.ready_time = 0
		stats.total_available_work_time_per_day += (avail_time_end - avail_time_start)
		
	
	
	def get_avail_time_sec(self):
		return 3600*(self.avail_time_end - self.ready_time)
	
		
  	def is_ready(self):
		t = utils.get_local_time_in_hours(self.timezone)
		if t >= self.avail_time_start and t < self.avail_time_end:
			if ((t - self.avail_time_start)*3600 < params.time_step-0.00001) or t >= self.ready_time:
				#first time in shift or inside the shift but past the ready_time
				#in both cases we just ignore the ready_time and set it to the current t
				self.ready_time = t
				return 1
			else:
				return 0

		#self.ready_time = self.avail_time_start
		return 0
				
      
	def print_worker(self):
		return "(" + str(self.id) + "," +str(self.skills)+","\
		+str(self.avail_time_start)+","\
		+str(self.avail_time_end)+","\
		+str(self.timezone)+","\
		+str(self.is_ready())+","\
		+str(utils.get_local_time_in_hours(self.timezone))+")"
        

		
		

