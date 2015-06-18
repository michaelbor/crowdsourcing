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
from multiprocessing import Process, Lock

#gen.generate_workers_db()
#gen.generate_steps_db()

if len(sys.argv) > 1:
	params.num_of_new_tasks_per_hour = int(sys.argv[1])

if len(sys.argv) > 2:
	params.algo_type = int(sys.argv[2])

algorithm = {\
#1:algo.allocate_jobs1, \
1:algo.allocate_jobs1, \
2:algo.allocate_jobs_skills_no_split, \
3:algo.allocate_jobs_steps_no_split}


workers_array = []
tasks_array = []

input.init_workers_from_db("workers_db.txt", workers_array)

w = len(workers_array)
print w
for i in range(0,w):
	stats.mutex.extend([Lock()])


stats.cur_time = params.time_step


input.load_steps_duration('avg_duration_result.txt')

f = open('join_result_ordered.txt', 'r')



f.readline()
input.load_samasource_data(tasks_array, f)


stats.t_start = time() #measuring running time of the simulation


for stats.iter in range(0, params.max_num_of_iterations):
			
	if stats.iter % 100 == 0:
		print '*** starting iteration '+str(stats.iter+1)+',  time: '+str(stats.cur_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(stats.total_steps_entered_system)+']'
		utils.print_statistics()			
		
	if utils.get_num_of_days_passed() > 500:# or (stats.total_backlog / (stats.iter+1)) > 500:
		break
		
	input.load_samasource_data(tasks_array, f)
	ready_workers = [x for x in workers_array if x.is_ready() == True]
	algorithm[params.algo_type](tasks_array, ready_workers)
	tasks_array = [x for x in tasks_array if False in (s.isCompleted for s in x.steps_array)]
	stats.total_backlog += (stats.total_steps_entered_system - stats.fully_scheduled_steps)
	stats.cur_time += params.time_step

stats.t_end = time()

f.close

print '=== final statistics ==='
utils.print_statistics()

'''
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
'''