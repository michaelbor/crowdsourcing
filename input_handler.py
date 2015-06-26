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
		

def load_steps_duration(filename):
	data = np.genfromtxt(filename, delimiter='|', skip_header = 3, \
			skip_footer = 1, autostrip = True,\
			dtype=[('step_id','i8'),('avg_duration','f8')])
	
	for line in data:
		stats.steps_avg_duration_dict[line['step_id']] = line['avg_duration']
	


def get_gen(line):
    yield line
            		
def load_samasource_data(tasks_array, f):

	if	stats.last_loaded_step_time > stats.cur_time:
		return
	
	
	task_prio = 1
	last_pos = f.tell()
	
	while 1:
		line = f.readline()
		if (stats.total_steps_entered_system - stats.fully_scheduled_steps) > params.buf:
			f.seek(last_pos)
			return	
			
		
		if line == '':
			stats.steps_file_ended = 1
			return
			
		if(len(line.split("|")) != 8):
			continue
							
		data = np.genfromtxt(get_gen(line), delimiter='|', autostrip = True,\
		dtype=[('step_id','i8'),('task_id','S50'), ('created_at','S50'),\
		('ordinal','i8'),('duration_gold','f8'),('duration','f8'),\
		('last_submission_at','S50'),('answered_at','S50')])
			
		
		if stats.total_steps_entered_system == 0:
			params.first_step_time = time.mktime(time.strptime(str(data['created_at']), '%Y-%m-%d %H:%M:%S'))
				
		arr_time = time.mktime(time.strptime(str(data['created_at']), '%Y-%m-%d %H:%M:%S')) \
					- params.first_step_time
					
		if(arr_time > stats.cur_time):
			stats.last_loaded_step_time = arr_time
			f.seek(last_pos)
			return
			
		
		if len(tasks_array) == 0 or tasks_array[-1].id != data['task_id']:
			new_task = Task(data['task_id'], task_prio)
			tasks_array.extend([new_task])
			last_submission_string = utils.prepare_submission_at(str(data['last_submission_at']))
			
						
			if str(data['last_submission_at']).strip() != '':
				first_submission_string = utils.prepare_submission_at(str(data['answered_at']))
				last_submission = time.mktime(time.strptime(last_submission_string, '%Y-%m-%d %H:%M:%S')) \
					- params.first_step_time
					
				first_submission = time.mktime(time.strptime(first_submission_string, '%Y-%m-%d %H:%M:%S')) \
					- params.first_step_time
				
				duration_of_first_step = float(data['duration'])
				turnaround_time = last_submission - (first_submission - duration_of_first_step)
			
				if turnaround_time < (params.max_task_turnaround_days * 24 * 3600):
					stats.samasource_tasks_entered += 1
					stats.samasource_tasks_total_tunaround += turnaround_time
					#print '****** '+str(data['task_id'])+'   '+str(stats.samasource_tasks_entered)
			
			
		s = Step(data['step_id'], \
		arr_time,\
		data['task_id'], \
		[[1,stats.steps_avg_duration_dict[int(data['step_id'])]]], task_prio, data['ordinal'])
			
		if s.order == 1:
			s.isLocked = False
				
		tasks_array[-1].add_step(s) #add step to the last task in the tasks_array
		#if(data['task_id'] == '524326f52d7bef2278005263' and s.order == 1):
		#	print "******inserting step of task 524326f52d7bef2278005263, step order: "+str(s.order)
		#	sys.exit()
		
		#if s.task_id == '524326fc2d7bef2278006801':
		#	print 'task id: '+str(s.task_id)+' ordinal: '+str(s.order)+' entering the system at time: '+str(stats.cur_time)

		stats.data_files_rows_read += 1
		last_pos = f.tell()
	
		
