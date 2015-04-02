from __future__ import division
import numpy as np
import algorithm_greedy as algo
import input_handler as input
import utils
import data_generator as gen
import stats
import params
from time import time 
#from task_class import Task
#from step_class import Step

#gen.random_steps_one_time()


workers_array = [] 
gen.random_workers()
input.init_workers_from_file('input_workers1.txt', workers_array)
#utils.print_all_workers(workers_array)

tasks_array = []
'''
tasks_array.extend([Task(1, 333)])
s = Step(135, 3.33, 1, [[2,20000],[3,400]], 333 ,1)
tasks_array[0].add_step(s)
tasks_array.extend([Task(0, 444)])
s = Step(160, 5.33, 0, [[2,20000],[3,400]], 333 ,1)
tasks_array[1].add_step(s)
utils.print_all_tasks(tasks_array)
'''

gen.random_steps()
input.init_steps_from_file('input_steps2.txt', tasks_array)
utils.print_all_tasks(tasks_array)



stats.t_start = time() #measuring running time of the simulation

stats.cur_time += params.time_step 

for i in range(0, params.max_num_of_iterations):
	
	if i % max(1, int(params.num_of_steps/100)) == 0:
		print '*** starting iteration '+str(i+1)+',  time: '+str(stats.cur_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(stats.total_steps_entered_system)+']'
		utils.print_statistics()
	
	'''
	if utils.is_all_steps_fully_scheduled(tasks_array):
		print '*** starting iteration '+str(i+1)+',  time: '+str(my_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(params.num_of_steps)+']'
		print '*** All steps are fully scheduled at iteration '+ str(i+1)+ '. Stopping simulation. ***\n'
		break
	'''	
	steps_for_allocation = utils.extract_steps_for_allocation(tasks_array)
	algo.allocate_jobs(steps_for_allocation, workers_array)
	#utils.print_steps(steps_for_allocation)
	
	utils.update_steps_status(tasks_array)
	utils.update_workers_status(workers_array)
	gen.random_workers()
	input.init_workers_from_file('input_workers1.txt', workers_array)
	gen.random_steps()
	input.init_steps_from_file('input_steps2.txt', tasks_array)
	
	utils.sort_tasks(tasks_array) #needed since the arr_time of a task may change
	
	stats.cur_time += params.time_step

stats.t_end = time()

#utils.print_all_tasks(tasks_array)
#utils.print_all_workers(workers_array)
utils.print_statistics()



#utils.print_all_tasks(tasks_array)