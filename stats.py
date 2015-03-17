
wasted_workers_time = 0

def avg_in_system_time(tasks_array):
	acc = 0
	count = 0
	for task in tasks_array:
		for step in task.steps_array:
			if step.isCompleted == True:
				acc = acc + step.in_system_time
				count = count + 1
	
	return round(acc/count,3)
	

def avg_work_time(tasks_array):
	acc = 0
	count = 0
	for task in tasks_array:
		for step in task.steps_array:
			if step.isCompleted == True:
				acc = acc + step.total_skills_time
				count = count + 1
	
	return round(acc/count,3)	