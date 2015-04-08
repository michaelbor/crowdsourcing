import utils
import stats
import params

def update_avail_time(workers_array):
	for worker in workers_array:
		worker.avail_time -= worker.used_time
		worker.used_time = 0
		
		
def reset_used_time(workers_array):
	for worker in workers_array:
		worker.used_time = 0


def is_step_fully_scheduled(step):
	for skills in step.skills:
		if skills[1] > 0:
			return False
			
	return True

				
def allocate_jobs(steps_array, workers_array):
	for step in steps_array:			
		for skill in step.skills:
			required_time = skill[1]
			temp_workers = []
			for worker in workers_array:
				if skill[0] in worker.skills:
					worker.used_time = min(worker.avail_time, required_time)
					required_time = required_time - worker.used_time
					temp_workers.extend([worker])
			
					if required_time == 0:
						#update_avail_time(workers_array)
						update_avail_time(temp_workers)
						step.timeToFinish = max(step.timeToFinish, skill[1])
						skill[1] = 0 #skill is allocated, clear its required time
						break
			
			if required_time > 0: 
				#reset_used_time(workers_array) #skill can't be allocated now.				
				reset_used_time(temp_workers)
		
		if is_step_fully_scheduled(step) == True:
			step.isFullyScheduled = True
			stats.fully_scheduled_steps += 1 
			step.in_system_time = stats.cur_time + step.timeToFinish - step.arr_time 
			stats.total_steps_in_system_time += step.in_system_time
			stats.total_work_time += step.total_skills_time
			stats.total_waiting_time += step.waiting_time

		elif step.timeToFinish == 0: #this means that no new skill is scheduled, i.e., pure waiting
			step.waiting_time += params.time_step
			
			
			
				
	#utils.print_steps_after_allocation(steps_array)		
	return	
	
		

def allocate_jobs_skills_no_split(steps_array, workers_array):
	for step in steps_array:			
		for skill in step.skills:
			for worker in workers_array:
				if skill[0] in worker.skills and worker.avail_time >= skill[1]:
					worker.used_time = skill[1]
					update_avail_time([worker])
					step.timeToFinish = max(step.timeToFinish, skill[1])
					skill[1] = 0 #skill is allocated, clear its required time
					break
		
		if is_step_fully_scheduled(step) == True:
			step.isFullyScheduled = True
			stats.fully_scheduled_steps += 1 
			step.in_system_time = stats.cur_time + step.timeToFinish - step.arr_time 
			stats.total_steps_in_system_time += step.in_system_time
			stats.total_work_time += step.total_skills_time
			stats.total_waiting_time += step.waiting_time

		elif step.timeToFinish == 0: #this means that no new skill is scheduled, i.e., pure waiting
			step.waiting_time += params.time_step
			
		
	return	
	
		 
        
    
		
		
		

