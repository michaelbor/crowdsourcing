import random
import params
import numpy as np


	
def random_steps():
	
	prev_time = 0
	steps_per_task = [0]* params.num_of_tasks
	tasks_prio = [0]* params.num_of_tasks

	thefile = open('input_steps1.txt', 'w')	
	thefile.write("#id, arr_time, task_id, skills, task_prio, order\n")

	for i in range(0, params.num_of_steps):
		id = i
		arr_time = round(prev_time + random.random() * params.arr_time_avg_gap, 1) 
		prev_time = arr_time
		num_of_skills = random.randint(1, params.max_num_of_skills)
		skills_seq = random.sample(range(1, params.max_num_of_skills + 1), num_of_skills)
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
	


def random_workers():
		
	thefile = open('input_workers1.txt', 'w')	
	thefile.write("#id, skills, avail_time\n")
	
	new_workers_per_time_step = (params.num_of_new_workers_per_hour * params.time_step) / 3600 
	num_of_workers = max(2, np.random.poisson(new_workers_per_time_step))
	
	for i in range(0, num_of_workers):
		id = i
		num_of_skills = random.randint(1, params.max_num_of_skills)
		skills_seq = random.sample(range(1, params.max_num_of_skills + 1), num_of_skills)
		avail_time = num_of_skills * random.randint(params.min_skill_time, params.max_skill_time)
		
		thefile.write("%s, " % id)
		
		skills_string = str(skills_seq)
		skills_string = skills_string.translate(None,' ')
		thefile.write(skills_string)
		
		thefile.write(", %s\n" % avail_time)
	
	thefile.close()
	
	
	
