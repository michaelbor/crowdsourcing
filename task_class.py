import stats
import params
import globals 

class Task:
	""" Class that represents any task """

	def __init__(self, id, task_prio, project_id=0):

		self.id = id
		self.project_id = project_id
		self.task_prio = task_prio
		self.arr_time = 0
		self.steps_array = []
		
	
        
	def print_task(self):
		return "(" + str(self.id) + "," + str(self.arr_time) + ","\
		+ str(self.task_prio) + ")"
	
			
	def print_task_steps(self):
		for s in self.steps_array:
			print s.print_step()
		
		
	def add_step(self, new_step):
		self.steps_array.extend([new_step])
		if self.arr_time == 0:
			self.arr_time = new_step.arr_time
		stats.total_steps_entered_system += 1
		
	def is_completed(self):
		if False in (s.isCompleted for s in self.steps_array):
			return False
		else:
			tat = max(s.finish_time for s in self.steps_array) - self.arr_time
			stats.total_tasks_turnaround_time += tat
			stats.total_finished_tasks += 1
			globals.our_algo_bins.insert(tat)
			if self.project_id in params.real_time_projects:
				stats.total_tasks_turnaround_time_realtime += tat
				stats.total_finished_tasks_realtime += 1
				globals.our_algo_bins_realtime.insert(tat)
			return True
			
	
		
	'''	
	def sort_steps_ordering(self):
		self.steps_array.sort(key=lambda x: x.arr_time)
		self.steps_array.sort(key=lambda x: x.order)
	'''
	'''	
	def set_task_arr_time(self):
		for i in self.steps_array:
			if i.isFullyScheduled == False:
				self.arr_time = i.arr_time
				return
				
		#print 'Info: all steps for task '+str(self.id)+' were completed'
		self.arr_time = -1
	'''	
		
		 
        
    
		
		
		

