from step_class import Step
from task_class import Task
from worker_class import Worker

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

				

def init_workers_from_file(data):
	workers_array=[]
	for i in range(0,len(data)):
		new_worker = Worker(data[i]['id'],\
		parse_skills_workers(data[i]['skills']),\
		data[i]['avail_time'])
		workers_array.extend([new_worker]);
		
	return workers_array
	
	
def init_steps_from_file(data):
	'''
	Initializing tasks dictionary that will hold all the tasks objects. 
	These objects can be accessible by task_id.
	'''
	tasks_dict = {}
	for i in range(0,len(data)):
		if tasks_dict.has_key(data[i]['task_id']) == False:
			tasks_dict[data[i]['task_id']] = Task(data[i]['task_id'], data[i]['task_prio'])
	
		s = Step(data[i]['id'], data[i]['arr_time'], data[i]['task_id'], parse_skills_steps(data[i]['skills']), data[i]['task_prio'],data[i]['order'])
		tasks_dict[data[i]['task_id']].add_step(s)
		
	#print ['num of distinct task ids: ',len(set(data[:]['task_id'])), "which is also: " ,len(tasks_dict)]

	'''
	From now we don't need the dictionary, but only a list. Since we will need to sort tasks.
	'''
	tasks_array = []
	tasks_array = tasks_dict.values()
	for i in tasks_array:
		i.sort_steps_ordering()
		i.set_task_arr_time()
	
	tasks_array.sort(key=lambda x: x.arr_time)
	tasks_array.sort(key=lambda x: x.task_prio,reverse=True)
	return tasks_array
	
		
