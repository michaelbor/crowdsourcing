import numpy as np
from step_class import Step
from task_class import Task
from worker_class import Worker
import utils
import stats
import os

def parse_skills_workers(skills_string):
	k = skills_string.translate(None,'[]')
	k = k.split(',')
	k = map(int,k)
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
	#if os.path.getsize(filename) > 0:
	data = np.genfromtxt(filename, delimiter=', ', \
	dtype=[('id','i8'), ('arr_time','f8'), ('task_id','i8'),\
	 ('skills','S5000'), ('task_prio','i8'), ('order','i8')])
	
	data_size = len(data)
		
	i = 0
	while i < data_size:
		new_task = Task(data[i]['task_id'], data[i]['task_prio'])
		s = Step(data[i]['id'], data[i]['arr_time'], data[i]['task_id'], \
		utils.parse_skills_steps(data[i]['skills']), data[i]['task_prio'],data[i]['order'])
		s.isLocked = False
		order_of_first = s.order
		new_task.add_step(s) #adding the first step of the task
		
		i += 1
		while i < data_size and data[i]['task_id'] == data[i-1]['task_id']:
			s = Step(data[i]['id'], data[i]['arr_time'], data[i]['task_id'], \
			parse_skills_steps(data[i]['skills']), data[i]['task_prio'],data[i]['order'])
			if s.order == order_of_first:
				step.isLocked = False
			
			new_task.add_step(s)
			i += 1
			
		tasks_array.extend([new_task])
		
		
	tasks_array.sort(key=lambda x: x.task_prio,reverse=True)
	

def init_workers_from_db(filename, workers_array):
	data = np.genfromtxt(filename, delimiter=', ', \
	dtype=[('id','i8'),('skills','S5000'), ('avail_time_start','i8'), \
	('avail_time_end','i8'), ('timezone','i8')])
		
	#notice, we assume that a worker always has the same set of skills
	for i in range(0,len(data)):
		new_worker = Worker(data[i]['id'],\
		parse_skills_workers(data[i]['skills']),\
		data[i]['avail_time_start'],\
		data[i]['avail_time_end'],\
		data[i]['timezone'])
		
		workers_array.extend([new_worker])
				
		#stats.total_available_work_time += data[i]['avail_time']
		
		
		
