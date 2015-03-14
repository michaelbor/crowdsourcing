
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


def print_steps_for_allocation(steps):
	print "printing steps for allocation:"
	print "---------------------------------------------"
	for i in steps:
		print i.print_step()
		
	print "---------------------------------------------\n"
	

def print_steps_after_allocation(steps):
	print "printing steps after allocation:"
	print "---------------------------------------------"
	for i in steps:
		print i.print_step()
		
	print "---------------------------------------------\n"

def extract_steps_for_allocation(tasks_array):
	steps_for_allocation=[]
	for task in tasks_array:
		for step in task.steps_array:
			if step.isCompleted == False:
				steps_for_allocation.extend([step])
			
	return steps_for_allocation
	
	
	