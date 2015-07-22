from __future__ import division
import random
import params
import stats
import numpy as np
from step_class import Step
from task_class import Task
import utils



def generate_steps_db(filename):

	thefile = open(filename, 'w')	
	thefile.write("#id, skills, ordinal\n")
	
	for i in range(0, params.num_of_steps_in_db):
		id = i
		ordinal = random.randint(1,params.max_ordinal)
		num_of_skills = random.randint(1, params.max_num_of_skills_steps)
		#skills_seq = random.sample(range(1, params.max_num_of_skills_steps + 1), num_of_skills)
		skills_seq = random.sample(range(1, params.num_of_existing_skills + 1), min(num_of_skills,params.num_of_existing_skills))
		skills = []
		for i in skills_seq:
			skills.extend([[i,random.randint(params.min_skill_time, params.max_skill_time)]])
			
		thefile.write("%s, " % id)
		skills_string = str(skills)
		skills_string = skills_string.translate(None,' ')
		thefile.write(skills_string)
		thefile.write(", ")
		thefile.write("%s\n" % ordinal)
	
	thefile.close()
		

def generate_workers_db(filename):

	thefile = open(filename, 'w')
	thefile.write("#id, skills, avail_time_start, avail_time_end, timezone\n")
	
	
	for i in range(0, params.num_of_workers_in_db):
		id = i
		num_of_skills = random.randint(1, params.max_num_of_skills_worker)
		skills_seq = random.sample(range(1, params.num_of_existing_skills + 1), min(num_of_skills,params.num_of_existing_skills))
		[avail_time_start, avail_time_end] = random.sample(params.working_hours, 1)[0]
		time_zone = random.sample(params.timezones,1)[0]
		thefile.write("%d, " % id)
		
		skills_string = str(skills_seq)
		skills_string = skills_string.translate(None,' ')
		thefile.write(skills_string)		
		thefile.write(", %d, %d, %.1f\n" % (avail_time_start, avail_time_end, time_zone))

	thefile.close()
	
	
		
'''	
def random_steps_one_time():
	
	prev_time = 0
	steps_per_task = [0]* params.num_of_tasks
	tasks_prio = [0]* params.num_of_tasks

	thefile = open('input_steps1.txt', 'w')	
	thefile.write("#id, arr_time, task_id, skills, task_prio, order\n")

	for i in range(0, params.num_of_steps):
		id = i
		arr_time = round(prev_time + random.random() * params.arr_time_avg_gap, 1) 
		prev_time = arr_time
		num_of_skills = random.randint(1, params.max_num_of_skills_steps)
		skills_seq = random.sample(range(1, params.max_num_of_skills_steps + 1), num_of_skills)
		skills = []
		for i in skills_seq:
			skills.extend([[i,random.randint(params.min_skill_time, params.max_skill_time)]])
			
		task_id = random.randint(0, params.num_of_tasks-1)
		if random.random() > params.fraction_of_unordered_steps: #e.g., in 10% of cases, we generate the same step's order
			steps_per_task[task_id] = steps_per_task[task_id] + 1
		order = steps_per_task[task_id]
		if tasks_prio[task_id] != 0:
			task_prio = tasks_prio[task_id]
		else:
			task_prio = random.randint(1, params.max_prio)
			tasks_prio[task_id] = task_prio
			
		line = [id, arr_time, task_id] 
		for i in range(0, len(line)):
			thefile.write("%s, " % line[i])
		
		skills_string = str(skills)
		skills_string = skills_string.translate(None,' ')
		thefile.write(skills_string)
		thefile.write(", ")
		
		line = [task_prio, order]
		for i in range(0, len(line)-1):
			thefile.write("%s, " % line[i])
		
		thefile.write("%s\n" % line[i+1])
			
	thefile.close()
	


def random_steps():
	
	prev_time = stats.cur_time
	steps_per_task = [0]* params.num_of_tasks
	tasks_prio = [0]* params.num_of_tasks

	new_steps_per_time_step = (params.num_of_new_steps_per_hour * params.time_step) / 3600 
	num_of_steps = max(2, np.random.poisson(new_steps_per_time_step))

	thefile = open('input_steps2.txt', 'w')	
	thefile.write("#id, arr_time, task_id, skills, task_prio, order\n")

	for i in range(0, num_of_steps):
		id = i + stats.total_steps_entered_system
		arr_time = round(prev_time + random.random() * params.arr_time_avg_gap, 1) 
		prev_time = arr_time
		num_of_skills = random.randint(1, params.max_num_of_skills_steps)
		skills_seq = random.sample(range(1, params.max_num_of_skills_steps + 1), num_of_skills)
		skills = []
		for i in skills_seq:
			skills.extend([[i,random.randint(params.min_skill_time, params.max_skill_time)]])
			
		task_id = random.randint(0, params.num_of_tasks-1)
		if random.random() > params.fraction_of_unordered_steps: #e.g., in 10% of cases, we generate the same step's order
			steps_per_task[task_id] = steps_per_task[task_id] + 1
		order = steps_per_task[task_id]
		if tasks_prio[task_id] != 0:
			task_prio = tasks_prio[task_id]
		else:
			task_prio = random.randint(1, params.max_prio)
			tasks_prio[task_id] = task_prio
			
		line = [id, arr_time, task_id] 
		for i in range(0, len(line)):
			thefile.write("%s, " % line[i])
		
		skills_string = str(skills)
		skills_string = skills_string.translate(None,' ')
		thefile.write(skills_string)
		thefile.write(", ")
		
		line = [task_prio, order]
		for i in range(0, len(line)-1):
			thefile.write("%s, " % line[i])
		
		thefile.write("%s\n" % line[i+1])
			
	thefile.close()
	
'''	




	
'''	
def random_steps_from_db(steps_db_filename):
	
	prev_time = stats.cur_time - params.time_step 
	
	data = np.genfromtxt(steps_db_filename, delimiter=', ', \
	dtype=[('id','i8'), ('skills','S5000'), ('order','i8')])
 	

	new_tasks_per_time_step = (params.num_of_new_tasks_per_hour * params.time_step) / 3600 
	num_of_tasks = max(2, np.random.poisson(new_tasks_per_time_step))
	
	if new_tasks_per_time_step < 2:
		print 'Warning: new_tasks_per_time_step = '+str(new_tasks_per_time_step)+'. Using at least 2.'

	thefile = open('input_steps_from_db.txt', 'w')	
	thefile.write("#id, arr_time, task_id, skills, task_prio, order\n")

	
	for i in range(0, num_of_tasks):
		
		task_id = stats.total_tasks_generated
		stats.total_tasks_generated += 1
		
		task_prio = random.randint(1, params.max_prio)
		
		steps_in_task = random.randint(1,params.max_ordinal)
		for j in range(0,steps_in_task):
			
			step_index = random.sample(np.where(data['order'] == j+1)[0], 1)
			arr_time = round(prev_time + random.random() * params.arr_time_avg_gap, 1)
			prev_time = arr_time
			line = [data['id'][step_index][0], arr_time, task_id] 
			
			for i in range(0, len(line)):
				thefile.write("%s, " % line[i])
		
			thefile.write(data['skills'][step_index][0])
			thefile.write(", ")
		
			line = [task_prio, data['order'][step_index][0]]
			for i in range(0, len(line)-1):
				thefile.write("%s, " % line[i])
		
			thefile.write("%s\n" % line[i+1])
			
	thefile.close()
'''	


'''
def random_workers():
		
	thefile = open('input_workers1.txt', 'w')	
	thefile.write("#id, skills, avail_time\n")
	
	new_workers_per_time_step = (params.num_of_new_workers_per_hour * params.time_step) / 3600 
	num_of_workers = max(2, np.random.poisson(new_workers_per_time_step))
	
	for i in range(0, num_of_workers):
		id = i
		num_of_skills = random.randint(1, params.max_num_of_skills_worker)
		skills_seq = random.sample(range(1, params.max_num_of_skills_worker + 1), num_of_skills)
		avail_time = random.randint(params.avail_time_avg - params.avail_time_avg/2, \
		params.avail_time_avg + params.avail_time_avg/2)
		
		thefile.write("%s, " % id)
		
		skills_string = str(skills_seq)
		skills_string = skills_string.translate(None,' ')
		thefile.write(skills_string)
		
		thefile.write(", %s\n" % avail_time)
	
	thefile.close()
'''	

'''
def random_workers_from_db(workers_db_filename):
		
	data = np.genfromtxt(workers_db_filename, delimiter=', ', \
	dtype=[('id','i8'),('skills','S5000'), ('avail_time','i8')])	
		
	thefile = open('input_workers_from_db.txt', 'w')	
	thefile.write("#id, skills, avail_time\n")
	
	new_workers_per_time_step = (params.num_of_new_workers_per_hour * params.time_step) / 3600 
	num_of_workers = max(2, np.random.poisson(new_workers_per_time_step))
	
	for i in range(0, num_of_workers):
		#random_worker_index = ??? #we need to insert workers that are not in the system?
		#or what should be the workers input process???
		thefile.write("%s" % str(data['id'][5])+ ", " + \
		str(data['skills'][5]) + ", " + str(data['avail_time'][5]) + "\n")
	
	thefile.close()
'''	
	
	
