from step_class import Step
from task_class import Task
from worker_class import Worker
import numpy as np
import algorithm_greedy as algo

data = np.genfromtxt('input_steps.txt', delimiter=', ', \
dtype=[('id','i8'), ('arr_time','f8'), ('task_id','i8'),\
 ('skills','S5000'), ('task_prio','i8'), ('order','i8')])

data_workers = np.genfromtxt('input_workers.txt', delimiter=', ', \
dtype=[('id','i8'),('skills','S5000'), ('avail_time','i8')])


def parse_skills_workers(skills_string):
	k = skills_string.translate(None,'[]')
	k = k.split(',')
	k = map(int,k)
	return k

def parse_skills(skills_string):
	k = skills_string.translate(None,'[]')
	k = k.split(',')
	k = map(int,k)
	k=[[k[2*i],k[2*i+1]] for i in range(len(k)/2)]
	return k
	
def extract_steps_for_allocation(tasks_array):
	steps_for_allocation=[]
	for task in tasks_array:
		for step in task.steps_array:
			if step.isCompleted == False:
				steps_for_allocation.extend([step])
			else:
				break
	
	return steps_for_allocation
				
#print parse_skills_workers(data_workers[0]['skills'])

workers_array=[]
for i in range(0,len(data_workers)):
	new_worker = Worker(data_workers[i]['id'],\
	parse_skills_workers(data_workers[i]['skills']),\
	data_workers[i]['avail_time'])
	workers_array.extend([new_worker]);
	

for i in workers_array:
	print 'worker: '+i.print_worker()


'''
Initializing tasks dictionary that will hold all the tasks objects. 
These objects can be accessible by task_id.
'''
tasks_dict = {};
for i in range(0,len(data)):
	if tasks_dict.has_key(data[i]['task_id']) == False:
		tasks_dict[data[i]['task_id']] = Task(data[i]['task_id'], data[i]['task_prio'])
	
	s = Step(data[i]['id'], data[i]['arr_time'], data[i]['task_id'], parse_skills(data[i]['skills']), data[i]['task_prio'],data[i]['order'])
	tasks_dict[data[i]['task_id']].add_step(s)
		
print ['num of distinct task ids: ',len(set(data[:]['task_id'])), "which is also: " ,len(tasks_dict)]


'''
From now we don't need the dictionary, but only a list. Since we will need to sort tasks.
'''

tasks_array = tasks_dict.values()

for i in tasks_array:
	i.sort_steps_ordering()
	i.set_task_arr_time()
	

tasks_array.sort(key=lambda x: x.arr_time)
tasks_array.sort(key=lambda x: x.task_prio,reverse=True)

for i in tasks_array:
	print "task_id: "+str(i.id)
	i.print_task_steps()
	print '========='


steps_for_allocation = extract_steps_for_allocation(tasks_array)


for i in steps_for_allocation:
	print i.print_step()


algo.allocate_jobs(steps_for_allocation, workers_array)



