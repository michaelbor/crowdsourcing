from __future__ import division
import numpy as np
import algorithm_greedy as algo
import input_handler as input
import utils
import data_generator as gen
import stats
import params
from time import time 

gen.random_steps_one_time()
gen.random_workers()


workers_array = [] 
input.init_workers_from_file('input_workers1.txt', workers_array)
#utils.print_all_workers(workers_array)

tasks_array = []
input.init_steps_from_file('input_steps1.txt', tasks_array)
#utils.print_all_tasks(tasks_array)

my_time = 0

t0 = time() #measuring running time of the simulation

for i in range(0, params.max_num_of_iterations):
	
	if i % max(1, int(params.num_of_steps/100)) == 0:
		print '*** starting iteration '+str(i+1)+',  time: '+str(my_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(params.num_of_steps)+']'
	
	
	if utils.is_all_steps_fully_scheduled(tasks_array):
		print '*** starting iteration '+str(i+1)+',  time: '+str(my_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(params.num_of_steps)+']'
		print '*** All steps are fully scheduled at iteration '+ str(i+1)+ '. Stopping simulation. ***\n'
		break
		
	steps_for_allocation = utils.extract_steps_for_allocation(tasks_array, my_time)
	#utils.print_steps(steps_for_allocation)
	#print len(steps_for_allocation)
	algo.allocate_jobs(steps_for_allocation, workers_array, my_time)
	#utils.print_steps(steps_for_allocation)
	
	utils.update_steps_status(tasks_array)
	utils.update_workers_status(workers_array)
	gen.random_workers()
	input.init_workers_from_file('input_workers1.txt', workers_array)
	
	utils.sort_tasks(tasks_array) #needed since the arr_time of a task may change
	
	my_time = my_time + params.time_step

t1 = time()

#utils.print_all_tasks(tasks_array)
#utils.print_all_workers(workers_array)



print '--------- statistics -----------------------------'
print 'steps: avg_in_system_time/avg_work_time = ' + \
str(round((stats.total_steps_in_system_time/stats.completed_steps)/(stats.total_work_time/stats.fully_scheduled_steps),3))
print 'workers: total_work_time/total_avail_time = ' + \
str(round(stats.total_work_time/stats.total_available_work_time,4)*100)+'%'
print 'running time: '+str(round(t1-t0,3))+' sec'
print '--------------------------------------------------\n'
utils.print_all_tasks(tasks_array)