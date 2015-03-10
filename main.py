from step_class import Step
from task_class import Task
import numpy as np

data = np.genfromtxt('input.txt', delimiter=', ', \
dtype=[('id','i8'), ('arr_time','f8'), ('task_id','i8'),\
 ('skills','S5000'), ('task_prio','i8'), ('order','i8')])



def parse_skills(skills_string):
	k = skills_string.translate(None,'[]')
	k = k.split(',')
	k = map(int,k)
	k=[[k[2*i],k[2*i+1]] for i in range(len(k)/2)]
	return k
	



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



