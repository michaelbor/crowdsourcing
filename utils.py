import stats
import params


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
	isPrevCompleted = True
	prevOrder = -1
	for task in tasks_array:
		for step in task.steps_array:
			if step.isFullyScheduled == False and \
			step.isLocked == False and \
			step.arr_time <= current_time:
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
			if step.isCompleted == False:
				step.timeToFinish = max(0, step.timeToFinish - params.time_step)
				if step.isFullyScheduled == True and step.timeToFinish == 0:
					step.isCompleted = True
					unlock_next_steps(step, task.steps_array)
	
	
	
def update_workers_status(workers_array):
	for worker in workers_array:
		worker.avail_time = max(0, worker.avail_time - params.time_step)
		stats.wasted_workers_time = stats.wasted_workers_time + \
		min(params.time_step, worker.avail_time)
		if worker.avail_time == 0:
			workers_array.remove(worker)
			
			
	
def sort_tasks(tasks_array):
	for task in tasks_array:
		task.set_task_arr_time()
	
	tasks_array.sort(key=lambda x: x.arr_time)
	tasks_array.sort(key=lambda x: x.task_prio,reverse=True)
	

def is_all_steps_fully_scheduled(tasks_array):
	for task in tasks_array:
		for step in task.steps_array:
			if step.isFullyScheduled == False:
				return False
			
	return True
		
	
	
	
	