import numpy as np
from step_class import Step
from task_class import Task
from worker_class import Worker
import utils
import stats
import os
import time
import sys
import params
import globals
import random



def parse_skills_workers(skills_string):
	k = skills_string.translate(None,'[]')
	k = k.split(',')
	k = map(int,k)
	return k

				
'''
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
'''		
	
	
def init_steps_from_file(filename, tasks_array):
	'''
	Initializing tasks dictionary that will hold all the tasks objects. 
	These objects can be accessible by task_id.
	'''
	
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
	('avail_time_end','i8'), ('timezone','f8')])
		
	for i in range(0,len(data)):
		new_worker = Worker(data[i]['id'],\
		parse_skills_workers(data[i]['skills']),\
		data[i]['avail_time_start'],\
		data[i]['avail_time_end'],\
		data[i]['timezone'])
		
		workers_array.extend([new_worker])
				
		

def load_steps_duration(filename):
	data = np.genfromtxt(filename, delimiter='|', skip_header = 3, \
			skip_footer = 1, autostrip = True,\
			dtype=[('step_id','i8'),('avg_duration','f8')])
	
	for line in data:
		stats.steps_avg_duration_dict[line['step_id']] = line['avg_duration']
	


def get_gen(line):
    yield line
            		
def load_samasource_data(tasks_array):

	if	stats.last_loaded_step_time > stats.cur_time:
		return
	
	if stats.steps_file_ended == 1:
		return
	
	task_prio = 0
	last_pos = globals.sama_tasks_file.tell()
	
	while 1:
		line = globals.sama_tasks_file.readline()	
		
		if line == '':
			stats.steps_file_ended = 1
			tat = utils.get_tat()
			if tat < (params.max_task_turnaround_days * 24 * 3600):
				stats.samasource_tasks_entered += 1
				stats.samasource_tasks_total_tunaround += tat
				globals.sama_bins.insert(tat)
				
				if globals.sama_cur_task_project_id in params.real_time_projects:
					stats.samasource_tasks_entered_realtime += 1
					stats.samasource_tasks_total_tunaround_realtime += tat
					globals.sama_bins_realtime.insert(tat)
					
			return
		
		
		dtype_list = [('step_id','i8'),('task_id','S50'), ('created_at','S50'),\
		('ordinal','i8'),('duration_gold','f8'),('duration','f8'),\
		('last_submission_at','S50'),('answered_at','S50'),('project_id','i8')]
			
		if(len(line.split("|")) != len(dtype_list)):
			continue
							
		data = np.genfromtxt(get_gen(line), delimiter='|', autostrip = True, dtype = dtype_list)
		
		if (stats.total_steps_entered_system - stats.fully_scheduled_steps) > params.buf and\
		tasks_array[-1].id != data['task_id']:
			globals.sama_tasks_file.seek(last_pos)
			return	
		
		if stats.total_steps_entered_system == 0:
			stats.first_step_time = time.mktime(time.strptime(str(data['created_at']), '%Y-%m-%d %H:%M:%S'))
				
		arr_time = time.mktime(time.strptime(str(data['created_at']), '%Y-%m-%d %H:%M:%S')) \
					- stats.first_step_time
					
		if(arr_time > stats.cur_time):
			stats.last_loaded_step_time = arr_time
			globals.sama_tasks_file.seek(last_pos)
			return
		
		
		tat = -1
		if len(tasks_array) == 0 or tasks_array[-1].id != data['task_id']:
		
			if globals.is_first_task == True:
				globals.is_first_task = False
			else:	
				tat = utils.get_tat()
				if tat < (params.max_task_turnaround_days * 24 * 3600):
					stats.samasource_tasks_entered += 1
					stats.samasource_tasks_total_tunaround += tat
					globals.sama_bins.insert(tat)
					
					if globals.sama_cur_task_project_id in params.real_time_projects:
						stats.samasource_tasks_entered_realtime += 1
						stats.samasource_tasks_total_tunaround_realtime += tat
						globals.sama_bins_realtime.insert(tat)
						
				

			ans_at_str = utils.prepare_submission_at(str(data['answered_at']))
			ans_at = time.mktime(time.strptime(ans_at_str, '%Y-%m-%d %H:%M:%S'))
			dur = float(data['duration'])
			globals.sama_cur_task_time.extend([[ans_at, dur]])
			globals.sama_cur_task_project_id = data['project_id']
			globals.sama_cur_task_created_at = time.mktime(time.strptime(str(data['created_at']), '%Y-%m-%d %H:%M:%S'))
		
			if data['project_id'] in params.real_time_projects:
				task_prio = 1
			new_task = Task(data['task_id'], task_prio, data['project_id'])
			tasks_array.extend([new_task])
			
			
		else:
			ans_at_str = utils.prepare_submission_at(str(data['answered_at']))
			ans_at = time.mktime(time.strptime(ans_at_str, '%Y-%m-%d %H:%M:%S'))
			dur = float(data['duration'])
			globals.sama_cur_task_time.extend([[ans_at, dur]])	
			
		s = Step(data['step_id'], \
		arr_time,\
		data['task_id'], \
		[[1,stats.steps_avg_duration_dict[int(data['step_id'])]]], task_prio, data['ordinal'])
			
		if s.order == 1:
			s.isLocked = False
				
		tasks_array[-1].add_step(s) #add step to the last task in the tasks_array
		
		last_pos = globals.sama_tasks_file.tell()
	


def load_steps_db_to_memory(steps_db_filename):
	globals.steps_db = np.genfromtxt(steps_db_filename, delimiter=', ', \
	dtype=[('id','i8'), ('skills','S5000'), ('order','i8')])
	

def generate_and_load_steps_from_db(tasks_array):

	prev_time = stats.cur_time - params.time_step 
	new_tasks_per_time_step = (params.num_of_new_tasks_per_hour * params.time_step) / 3600 
	num_of_tasks = np.random.poisson(new_tasks_per_time_step)

	for i in range(0, num_of_tasks):
		
		task_id = stats.total_tasks_generated
		stats.total_tasks_generated += 1
		
		task_prio = random.randint(1, params.max_prio)
		
		new_task = Task(task_id, task_prio)
		
		steps_in_task = random.randint(1,params.max_ordinal)
		for j in range(0,steps_in_task):
			
			step_index = random.sample(np.where(globals.steps_db['order'] == j+1)[0], 1)
			arr_time = round(prev_time + random.random() * params.arr_time_avg_gap, 1)
			prev_time = arr_time
			s = Step(globals.steps_db['id'][step_index][0], arr_time, task_id, \
			utils.parse_skills_steps(globals.steps_db['skills'][step_index][0]), task_prio, globals.steps_db['order'][step_index][0])
			if j == 0:
				order_of_first = s.order
			if 	s.order == order_of_first:
				s.isLocked = False
			
			new_task.add_step(s)
			
		tasks_array.extend([new_task])
		#utils.print_all_tasks([new_task])
	
			
