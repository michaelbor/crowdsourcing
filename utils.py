from __future__ import division
import stats
import params
from time import time



def print_all_tasks(tasks_array):
	print "printing all tasks:"
	print "---------------------------------------------"
	for i in tasks_array:
		print "task_id: "+str(i.id)
		i.print_task_steps()
		print ''
		
	print "---------------------------------------------\n"


def print_all_workers(workers_array):
	print "printing all workers:"
	print "---------------------------------------------"
	for i in workers_array:
		print 'worker: '+i.print_worker()
		
	print "---------------------------------------------\n"




def print_steps(steps):
	print "printing steps:"
	print "---------------------------------------------"
	for i in steps:
		print i.print_step()
		
	print "---------------------------------------------\n"

def extract_steps_for_allocation(tasks_array, current_time):
	steps_for_allocation=[]
	for task in tasks_array:
		for step in task.steps_array:
			if step.isLocked == True:
				break
			elif step.isFullyScheduled == False and step.arr_time <= current_time:
				steps_for_allocation.extend([step])
					
	return steps_for_allocation
	
	
def unlock_next_steps(cur_step, steps_array):
	idx = steps_array.index(cur_step)
	if idx == len(steps_array) - 1:
		return
	if cur_step.order < steps_array[idx+1].order:
		order_of_first = steps_array[idx+1].order	
		for i in range(idx+1, len(steps_array)):
			if steps_array[i].order == order_of_first:
				steps_array[i].isLocked = False
			else:
				break
	


	
def update_steps_status(tasks_array):
	for task in tasks_array:
		for step in task.steps_array:
			if step.isLocked == True:
				break
			elif step.isCompleted == False:
				step.timeToFinish = max(0, step.timeToFinish - params.time_step)
				if step.isFullyScheduled == True and step.timeToFinish == 0:
					step.isCompleted = True
					stats.completed_steps += 1
					stats.total_steps_in_system_time += step.in_system_time
					unlock_next_steps(step, task.steps_array)
					task.steps_array.remove(step)
					
		if len(task.steps_array) == 0:
			tasks_array.remove(task)
	
	
	
def update_workers_status(workers_array):
	for worker in workers_array:
		stats.wasted_workers_time = stats.wasted_workers_time + \
		min(params.time_step, worker.avail_time)
		worker.avail_time = max(0, worker.avail_time - params.time_step)
		if worker.avail_time == 0:
			workers_array.remove(worker)
			
			
	
def sort_tasks(tasks_array):
	for task in tasks_array:
		task.set_task_arr_time()
	
	tasks_array.sort(key=lambda x: x.arr_time)
	tasks_array.sort(key=lambda x: x.task_prio,reverse=True)
	

def is_all_steps_fully_scheduled(tasks_array):
	#for task in tasks_array:
	#	for step in task.steps_array:
	#		if step.isFullyScheduled == False:
	#			return False
	if stats.fully_scheduled_steps == params.num_of_steps:
		return True
	else:
		return False
		

def print_statistics():
	print '--------- statistics -----------------------------'
	if stats.completed_steps > 0 and stats.total_work_time > 0 and stats.fully_scheduled_steps > 0:
		print 'steps: avg_in_system_time/avg_work_time = ' + \
		str(round((stats.total_steps_in_system_time/stats.completed_steps)/(stats.total_work_time/stats.fully_scheduled_steps),3))
		
	
	if stats.total_available_work_time > 0:
		print 'workers: total_work_time/total_avail_time = ' + \
		str(round(stats.total_work_time/stats.total_available_work_time,8)*100)+'%'
	
	print 'running time: '+str(round(time()-stats.t_start,3))+' sec'
	print '--------------------------------------------------\n'	
	
	
	