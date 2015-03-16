import random

def random_steps(n, m):
	prev_time = 0
	steps_per_task = [0]*m
	tasks_prio = [0]*m

	thefile = open('input_steps1.txt', 'w')	
	thefile.write("#id, arr_time, task_id, skills, task_prio, order\n")

	for i in range(0,n):
		id = i
		arr_time = round(prev_time + random.random() * 10, 1) 
		prev_time = arr_time
		num_of_skills = random.randint(1,3)
		skills_seq = random.sample(range(1,4), num_of_skills)
		skills = []
		for i in skills_seq:
			skills.extend([[i,random.randint(500,6000)]])
			
		task_id = random.randint(0,m-1)
		if random.random() > 0.1: #in 10% of cases, we generate the same step's order
			steps_per_task[task_id] = steps_per_task[task_id] + 1
		order = steps_per_task[task_id]
		if tasks_prio[task_id] != 0:
			task_prio = tasks_prio[task_id]
		else:
			task_prio = random.randint(1,20)
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