from __future__ import division
import utils
import stats
import params
import random


def update_avail_time(workers_array):
	for worker in workers_array:
		worker.ready_time += worker.used_time
		stats.new_total_work_time += worker.used_time
		worker.used_time = 0
		
		
def reset_used_time(workers_array):
	for worker in workers_array:
		worker.used_time = 0 #maybe this is not necessary since we never use "used_time" before setting it again


def is_step_fully_scheduled(step):
	for skills in step.skills:
		if skills[1] > 0:
			return False
			
	return True



def allocate_jobs1(tasks_array, workers_array):

	for task in tasks_array:
		for step in task.steps_array:
			res = utils.get_step_status(task, step)
			if res == 1:
				break
			if res == 2:
				continue			
			for skill in step.skills:
				required_time = skill[1]
				temp_workers = []
				random.shuffle(workers_array)
				#first_worker_index = random.randint(0,len(workers_array)-1)
				#worker_index = first_worker_index
				#while 1:
				#	worker = workers_array[worker_index]
				for worker in workers_array:
					if skill[0] in worker.skills and skill[1] > 0:
						worker.used_time = min(worker.get_avail_time_sec(), required_time)
						required_time -= worker.used_time
						temp_workers.extend([worker])
			
						if required_time == 0:	
							update_avail_time(temp_workers)	
							step.finish_time = max(max(w.ready_time for w in temp_workers),step.finish_time)
							skill[1] = 0 #skill is allocated, clear its required time
							break
							
					#worker_index += 1
					#worker_index = worker_index % len(workers_array)
					#if worker_index == first_worker_index:
					#	break
			
				if required_time > 0: 			
					reset_used_time(temp_workers) #skill can't be allocated now.
		
			if is_step_fully_scheduled(step) == True:
				step.isFullyScheduled = True
				stats.fully_scheduled_steps += 1 
			
	

def allocate_jobs_skills_no_split(tasks_array, workers_array):
	for task in tasks_array:
		for step in task.steps_array:
			res = utils.get_step_status(task, step)
			if res == 1:
				break
			if res == 2:
				continue
	
			for skill in step.skills:
				random.shuffle(workers_array)
				for worker in workers_array:
					if skill[0] in worker.skills and worker.get_avail_time_sec() >= skill[1]:
						worker.used_time = skill[1]
						update_avail_time([worker])
						step.finish_time = max(max(w.ready_time for w in [worker]),step.finish_time)
						skill[1] = 0 #skill is allocated, clear its required time
						break
		
			if is_step_fully_scheduled(step) == True:
				step.isFullyScheduled = True
				stats.fully_scheduled_steps += 1 
				

def allocate_jobs_steps_no_split(tasks_array, workers_array):
	for task in tasks_array:
		for step in task.steps_array:
			res = utils.get_step_status(task, step)
			if res == 1:
				break
			if res == 2:
				continue
	
			step_skills_array = [x[0] for x in step.skills]
			random.shuffle(workers_array)		
			for worker in workers_array:
				if set(step_skills_array).issubset(worker.skills) is True and\
				worker.get_avail_time_sec() >= step.total_skills_time:
					worker.used_time = step.total_skills_time
					update_avail_time([worker])
					step.finish_time = max(max(w.ready_time for w in [worker]),step.finish_time)
					for skill in step.skills:
						skill[1] = 0
				
					step.isFullyScheduled = True
					stats.fully_scheduled_steps += 1 
					break


		 
        
    
		
		
		

