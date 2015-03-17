import random



max_num_of_skills = 3
max_skill_time = 6000
min_skill_time = 500
	
def random_steps(num_of_steps, num_of_tasks):

	arr_time_var = 10
	max_prio = 20
	fraction_of_unordered_steps = 0.9
	
	prev_time = 0
	steps_per_task = [0]*num_of_tasks
	tasks_prio = [0]*num_of_tasks

	thefile = open('input_steps1.txt', 'w')	
	thefile.write("#id, arr_time, task_id, skills, task_prio, order\n")

	for i in range(0,num_of_steps):
		id = i
		arr_time = round(prev_time + random.random() * arr_time_var, 1) 
		prev_time = arr_time
		num_of_skills = random.randint(1,max_num_of_skills)
		skills_seq = random.sample(range(1,max_num_of_skills + 1), num_of_skills)
		skills = []
		for i in skills_seq:
			skills.extend([[i,random.randint(min_skill_time, max_skill_time)]])
			
		task_id = random.randint(0,num_of_tasks-1)
		if random.random() > fraction_of_unordered_steps: #in 10% of cases, we generate the same step's order
			steps_per_task[task_id] = steps_per_task[task_id] + 1
		order = steps_per_task[task_id]
		if tasks_prio[task_id] != 0:
			task_prio = tasks_prio[task_id]
		else:
			task_prio = random.randint(1,max_prio)
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
	


def random_workers(num_of_workers):
		
	thefile = open('input_workers1.txt', 'w')	
	thefile.write("#id, skills, avail_time\n")
	
	for i in range(0,num_of_workers):
		id = i
		num_of_skills = random.randint(1,max_num_of_skills)
		skills_seq = random.sample(range(1,max_num_of_skills + 1), num_of_skills)
		avail_time = num_of_skills * random.randint(min_skill_time, max_skill_time)
		
		thefile.write("%s, " % id)
		
		skills_string = str(skills_seq)
		skills_string = skills_string.translate(None,' ')
		thefile.write(skills_string)
		
		thefile.write(", %s\n" % avail_time)
	
	thefile.close()
	
	
	
