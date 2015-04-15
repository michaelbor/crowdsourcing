import numpy as np
from step_class import Step
from task_class import Task
from worker_class import Worker
import utils
import stats

def parse_skills_workers(skills_string):
	k = skills_string.translate(None,'[]')
	k = k.split(',')
	k = map(int,k)
	return k


def parse_skills_steps(skills_string):
	k = skills_string.translate(None,'[]')
	k = k.split(',')
	k = map(int,k)
	k=[[k[2*i],k[2*i+1]] for i in range(len(k)/2)]
	return k

				

def init_workers_from_file(filename, workers_array):
	data = np.genfromtxt(filename, delimiter=', ', \
	dtype=[('id','i8'),('skills','S5000'), ('avail_time','i8')])
	
	#first, let's read everything into dictionary in order to combine workers with the same id	
	workers_dict = {}
	for worker in workers_array:
		workers_dict[worker.id] = worker
		
	#notice, we assume that a worker always has the same set of skills
	for i in range(0,len(data)):
		if workers_dict.has_key(data[i]['id']) == False:
			new_worker = Worker(data[i]['id'],\
			parse_skills_workers(data[i]['skills']),\
			data[i]['avail_time'])
			workers_dict[data[i]['id']] = new_worker
		else:
			workers_dict[data[i]['id']].avail_time += data[i]['avail_time']
				
		stats.total_available_work_time += data[i]['avail_time']
		
	del workers_array[:]
	for worker in workers_dict.values():
		workers_array.extend([worker])
		
	
	
def init_steps_from_file(filename, tasks_array):
	'''
	Initializing tasks dictionary that will hold all the tasks objects. 
	These objects can be accessible by task_id.
	'''
	data = np.genfromtxt(filename, delimiter=', ', \
	dtype=[('id','i8'), ('arr_time','f8'), ('task_id','i8'),\
 	('skills','S5000'), ('task_prio','i8'), ('order','i8')])
	tasks_dict = {}
	
	#insert here to the dictionary the tasks from tasks_array !!!!!
	for task in tasks_array:
		tasks_dict[task.id] = task
	
	#clear the task_array
	del tasks_array[:]
	
	for i in range(0,len(data)):
		if tasks_dict.has_key(data[i]['task_id']) == False:
			tasks_dict[data[i]['task_id']] = Task(data[i]['task_id'], data[i]['task_prio'])
	
		s = Step(data[i]['id'], data[i]['arr_time'], data[i]['task_id'], \
		parse_skills_steps(data[i]['skills']), data[i]['task_prio'],data[i]['order'])
		tasks_dict[data[i]['task_id']].add_step(s)
		stats.total_steps_entered_system += 1
		
	'''
	From now we don't need the dictionary, but only a list. Since we will need to sort tasks.
	'''
	for task in tasks_dict.values():
		tasks_array.extend([task])
		
	for i in tasks_array:
		i.sort_steps_ordering()
		# now lets unlock first step of each task
		order_of_first = i.steps_array[0].order
		for step in i.steps_array:
			if step.order == order_of_first:
				step.isLocked = False
			else:
				break
	
	utils.sort_tasks(tasks_array)
	
	
		
