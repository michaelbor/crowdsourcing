from __future__ import division

wasted_workers_time = 0
total_available_work_time = 0
total_work_time = 0

def avg_in_system_time(tasks_array):
	acc = 0
	count = 0
	for task in tasks_array:
		for step in task.steps_array:
			if step.isCompleted == True:
				acc = acc + step.in_system_time
				count = count + 1
	
	if acc == 0:
		return 0
	else:
		return round(acc/count,3)
	

def avg_and_total_work_time(tasks_array):
	acc = 0
	count = 0
	for task in tasks_array:
		for step in task.steps_array:
			if step.isFullyScheduled == True:
				acc = acc + step.total_skills_time
				count = count + 1
	
	if acc == 0:
		return [0, 0]
	else:
		return [round(acc/count,3), acc]	
		

def total_avail_time(workers_array):
	acc = 0
	for worker in workers_array:
		acc = acc + worker.avail_time
		
	return acc
	
	
	