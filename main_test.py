from __future__ import division
import numpy as np
import algorithm_greedy as algo
import input_handler as input
import utils
import data_generator as gen
import stats
import params
from time import time


#gen.generate_workers_db()

workers_array = []
input.init_workers_from_db("workers_db.txt", workers_array)

#utils.print_all_workers(workers_array)
ready_workers = utils.get_ready_workers(workers_array)
#utils.print_all_workers(ready_workers)
print len(ready_workers)
print stats.total_available_work_time_per_day

gen.generate_steps_db()
gen.random_steps_from_db('steps_db.txt')



tasks_array = []
input.init_steps_from_file('input_steps_from_db.txt', tasks_array)



stats.t_start = time() #measuring running time of the simulation

stats.cur_time += params.time_step 

for i in range(0, params.max_num_of_iterations):
	
	if i % 100 == 0:
		print '*** starting iteration '+str(i+1)+',  time: '+str(stats.cur_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(stats.total_steps_entered_system)+']'
		utils.print_statistics()
	
	ready_workers = utils.get_ready_workers(workers_array)
	steps_for_allocation = utils.extract_steps_for_allocation(tasks_array)
	
	#algo.allocate_jobs(steps_for_allocation, ready_workers)
	algo.allocate_jobs_skills_no_split(steps_for_allocation, ready_workers)
	#algo.allocate_jobs_steps_no_split(steps_for_allocation, ready_workers)
	
	utils.update_steps_status(tasks_array)
	
	gen.random_steps_from_db('steps_db.txt')
	input.init_steps_from_file('input_steps_from_db.txt', tasks_array)
	
	utils.sort_tasks(tasks_array) #needed since the arr_time of a task may change
	
	stats.cur_time += params.time_step

stats.t_end = time()

utils.print_statistics()

