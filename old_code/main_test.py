from __future__ import division
import numpy as np
import algorithm_greedy as algo
import input_handler as input
import utils
import data_generator as gen
import stats
import params
from time import time
import sys
import os.path


#gen.generate_workers_db()
#gen.generate_steps_db()

if len(sys.argv) > 1:
	params.num_of_new_tasks_per_hour = int(sys.argv[1])

if len(sys.argv) > 2:
	params.algo_type = int(sys.argv[2])

algorithm = {\
1:algo.allocate_jobs, \
2:algo.allocate_jobs_skills_no_split, \
3:algo.allocate_jobs_steps_no_split}


workers_array = []
input.init_workers_from_db("workers_db.txt", workers_array)

ready_workers = utils.get_ready_workers(workers_array)

#gen.random_steps_from_db('steps_db.txt')

steps_db = gen.load_steps_db_to_memory('steps_db.txt')

stats.cur_time += params.time_step 

tasks_array = []
#input.init_steps_from_file('input_steps_from_db.txt', tasks_array)



stats.t_start = time() #measuring running time of the simulation



for stats.iter in range(0, params.max_num_of_iterations):
	
	if stats.iter % 100 == 0:
		print '*** starting iteration '+str(stats.iter+1)+',  time: '+str(stats.cur_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(stats.total_steps_entered_system)+']'
		utils.print_statistics()
		
	if utils.get_num_of_days_passed() > 5:# or (stats.total_backlog / (stats.iter+1)) > 500:
		break
		
	#gen.random_steps_from_db('steps_db.txt')
	#input.init_steps_from_file('input_steps_from_db.txt', tasks_array)	
	gen.generate_and_load_steps_from_db(steps_db, tasks_array)
	ready_workers = utils.get_ready_workers(workers_array)
	steps_for_allocation = utils.extract_steps_for_allocation_and_update_steps(tasks_array)
	
	algorithm[params.algo_type](steps_for_allocation, ready_workers)
	
	stats.total_backlog += (stats.total_steps_entered_system - stats.fully_scheduled_steps)
	#utils.update_steps_status(tasks_array)
	stats.cur_time += params.time_step

stats.t_end = time()

print '=== final statistics ==='
utils.print_statistics()

if os.path.isfile('results.txt') == False:
	thefile = open('results.txt', 'a')
	thefile.write("#algo load(tasks/h) wait_time      backlog utilization  days_passed\n")
else:
	thefile = open('results.txt', 'a')

#params.algo_type
#params.num_of_new_tasks_per_hour
#str(round(stats.total_waiting_time/stats.fully_scheduled_steps,3))
#str(stats.total_steps_entered_system - stats.fully_scheduled_steps)
#str(round(stats.new_total_work_time/(stats.total_available_work_time_per_day*(get_num_of_days_passed()))/3600,5)*100)


thefile.write("%s %6s %19s %10s %11s %8s\n" % (\
params.algo_type,\
params.num_of_new_tasks_per_hour,\
round(stats.total_waiting_time/stats.fully_scheduled_steps,3),\
round(stats.total_backlog / stats.iter,2),\
round(stats.new_total_work_time/(stats.total_available_work_time_per_day*(utils.get_num_of_days_passed()))/3600,5)*100,\
round(utils.get_num_of_days_passed(),2)))

thefile.close()