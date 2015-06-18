from __future__ import division
import utils
import stats
import params
import random
from multiprocessing import Process, Lock

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
				for worker in workers_array:
					if skill[0] in worker.skills and skill[1] > 0:
						worker.used_time = min(worker.get_avail_time_sec(), required_time)
						required_time -= worker.used_time
						temp_workers.extend([worker])
			
						if required_time == 0:	
							update_avail_time(temp_workers)	
							step.finish_time = max(max(w.ready_time for w in temp_workers),step.finish_time)
							skill[1] = 0 #skill is allocated, clear its required time
							#print 'step finish time: '+str(step.finish_time)
							#for w in temp_workers:
							#	print w.print_worker()
							break
			
				if required_time > 0: 			
					reset_used_time(temp_workers) #skill can't be allocated now.
		
			if is_step_fully_scheduled(step) == True:
				step.isFullyScheduled = True
				#print 'fully scheduled step '+str(step.id)+' of task '+str(task.id)
				stats.fully_scheduled_steps += 1 
				step.in_system_time = step.finish_time - step.arr_time 
				stats.total_steps_in_system_time += step.in_system_time
				stats.total_work_time += step.total_skills_time
				stats.total_waiting_time += step.waiting_time
				if step.task_id == '524326fc2d7bef2278006801':
					print 'task id: '+str(step.task_id)+' arr_time: '+str(step.arr_time)+' waiting time: '+str(step.waiting_time)+' ordinal: '+str(step.order) + ' cur_time: '+str(stats.cur_time)
			

			elif step.finish_time <= stats.cur_time: #this means that no new skill is scheduled, i.e., pure waiting
				step.waiting_time += params.time_step
							
	return	
	

def allocate_jobs(steps_array, workers_array):
	for step in steps_array:			
		for skill in step.skills:
			required_time = skill[1]
			temp_workers = []
			for worker in workers_array:
				#if worker.get_avail_time_sec() == 0:
				#	workers_array.remove(worker)
				if skill[0] in worker.skills and skill[1] > 0:
					worker.used_time = min(worker.get_avail_time_sec(), required_time)
					required_time -= worker.used_time
					temp_workers.extend([worker])
			
					if required_time == 0:	
						#skill finish time is the finish time of the worker who took the 
						#largest part of the skill				
						#skill_finish_time = max(w.used_time for w in temp_workers)
						#skill_finish_time = max(w.ready_time for w in temp_workers) - stats.cur_time
						step.finish_time = max(max(w.ready_time for w in temp_workers),step.finish_time)
						update_avail_time(temp_workers)	
						#step.timeToFinish = max(step.timeToFinish, skill_finish_time)#skill[1])
						skill[1] = 0 #skill is allocated, clear its required time
						break
			
			
			#workers_array = [x for x in workers_array if worker.get_avail_time_sec() > 0]
			if required_time > 0: 			
				reset_used_time(temp_workers) #skill can't be allocated now.
		
		if is_step_fully_scheduled(step) == True:
			step.isFullyScheduled = True
			stats.fully_scheduled_steps += 1 
			step.in_system_time = step.finish_time - step.arr_time 
			stats.total_steps_in_system_time += step.in_system_time
			stats.total_work_time += step.total_skills_time
			stats.total_waiting_time += step.waiting_time
			if step.task_id == '524326fc2d7bef2278006801':
				print 'task id: '+str(step.task_id)+' arr_time: '+str(step.arr_time)+' waiting time: '+str(step.waiting_time)+' ordinal: '+str(step.order) + ' cur_time: '+str(stats.cur_time)
			

		elif step.finish_time <= stats.cur_time: #this means that no new skill is scheduled, i.e., pure waiting
			step.waiting_time += params.time_step
							
	return	
	


def allocate_jobs_skills_no_split(steps_array, workers_array):
	for step in steps_array:			
		for skill in step.skills:
			for worker in workers_array:
				if skill[0] in worker.skills and worker.get_avail_time_sec() >= skill[1]:
					worker.used_time = skill[1]
					update_avail_time([worker])
					#step.timeToFinish = max(step.timeToFinish, skill[1])
					step.finish_time = max(max(w.ready_time for w in temp_workers),step.finish_time)
					skill[1] = 0 #skill is allocated, clear its required time
					break
		
		if is_step_fully_scheduled(step) == True:
			step.isFullyScheduled = True
			stats.fully_scheduled_steps += 1 
			step.in_system_time = step.finish_time + step.timeToFinish
			stats.total_steps_in_system_time += step.in_system_time
			stats.total_work_time += step.total_skills_time
			stats.total_waiting_time += step.waiting_time

		elif step.finish_time <= stats.cur_time: #this means that no new skill is scheduled, i.e., pure waiting
			step.waiting_time += params.time_step
				
	return	



def allocate_jobs_steps_no_split(steps_array, workers_array):
	for step in steps_array:			
		step_skills_array = []
		for skill in step.skills:
			step_skills_array.extend([skill[0]])
					
		for worker in workers_array:
			
			if set(step_skills_array).issubset(worker.skills) is True and\
			worker.get_avail_time_sec() >= step.total_skills_time:
				worker.used_time = step.total_skills_time
				update_avail_time([worker])
				#step.timeToFinish = max(step.timeToFinish, step.total_skills_time)
				step.finish_time = max(max(w.ready_time for w in temp_workers),step.finish_time)
				for skill in step.skills:
					skill[1] = 0
				
				step.isFullyScheduled = True
				stats.fully_scheduled_steps += 1 
				step.in_system_time = step.finish_time + step.timeToFinish
				stats.total_steps_in_system_time += step.in_system_time
				stats.total_work_time += step.total_skills_time
				stats.total_waiting_time += step.waiting_time
				break

		if step.finish_time <= stats.cur_time: #this means that no new skill is scheduled, i.e., pure waiting
				step.waiting_time += params.time_step
				
	return	

		 
        
    
		
		
		

