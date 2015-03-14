
class Step:
	""" Class that represents any step """

	def __init__(self, id, arr_time, task_id, skills, task_prio, order):

		self.id = id
		self.arr_time = arr_time
		self.task_id = task_id
		self.skills = skills
		self.isCompleted = False
		self.task_prio = task_prio
		self.order = order
				
        
	def print_step(self):
		return "(" + str(self.id) + "," + str(self.arr_time) + ","\
		+ str(self.task_id) + "," +str(self.skills)+","\
		+str(self.task_prio)+","+str(self.order)+") comp: "+str(self.isCompleted)
        
    
		
		
		

