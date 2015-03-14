import utils

def update_avail_time(workers_array):
	for worker in workers_array:
		worker.avail_time = worker.avail_time - worker.used_time
		worker.used_time = 0
		
		
def reset_used_time(workers_array):
	for worker in workers_array:
		worker.used_time = 0


def is_step_completed(step):
	for skills in step.skills:
		if skills[1] > 0:
			return False
			
	return True

				
def allocate_jobs(steps_array, workers_array):

	for step in steps_array:
		for skill in step.skills:
			required_time = skill[1]
			for worker in workers_array:
				if skill[0] in worker.skills:
					worker.used_time = min(worker.avail_time, required_time)
					required_time = required_time - worker.used_time
					
					if required_time == 0:
						update_avail_time(workers_array)
						skill[1] = 0 #skill is allocated, clear its required time
						break
			
			if required_time > 0: 
				reset_used_time(workers_array) #skill can't be allocated now. 
		
		if is_step_completed(step) == True:
			step.isCompleted = True 
				
	utils.print_steps_after_allocation(steps_array)		
	return	
	
		

		
		 
        
    
		
		
		

