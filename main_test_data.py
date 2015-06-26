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
from optparse import OptionParser



parser = OptionParser()
parser.add_option("--tasks_per_hour", dest="num_of_new_tasks_per_hour",type="int", default = 100,
                  help="number of new tasks per hour", metavar="NUM_OF_TASKS")
                  
parser.add_option("--algo", dest="algo_type",type="int", default = 1,
                  help="algorithm type: 1 - split skill level\n, 2 - split on step level\n, 3 - split on task level", metavar="ALGO")
                  
parser.add_option("--workers", dest="workers_file", default = "../data/workers_db.txt",
                  help="file with list of workers and their availability times", metavar="FILE")

parser.add_option("--avg_steps_duration", dest="avg_steps_duration_file", default = "../data/avg_duration_result.txt",
                  help="file with duration per step - needed when using the samasource data input", metavar="FILE")

parser.add_option("--tasks", dest="tasks_input_file", default = "../data/join_result_ordered.txt",
                  help="file that contains list of steps/tasks to schedule", metavar="FILE")
       
parser.add_option("--buf", dest="buf",type="int", default = 20000,
                  help="Buffer size - limits burst size - max number of tasks can be stored in the tasks_array", metavar="BUF_SIZE")                  

parser.add_option("--time_step", dest="time_step",type="int", default = 600,
                  help="Time step - time between consequitive schedulings", metavar="TIME_STEP")                  


(options, args) = parser.parse_args()

params.num_of_new_tasks_per_hour = options.num_of_new_tasks_per_hour
params.algo_type = options.algo_type
params.buf = options.buf
params.time_step = options.time_step


#gen.generate_workers_db()
#gen.generate_steps_db()



algorithm = {\
1:algo.allocate_jobs1, \
2:algo.allocate_jobs_skills_no_split, \
3:algo.allocate_jobs_steps_no_split}


workers_array = []
tasks_array = []

input.init_workers_from_db(options.workers_file, workers_array)



stats.cur_time = params.time_step


input.load_steps_duration(options.avg_steps_duration_file)

f = open(options.tasks_input_file, 'r')
f.readline() #skip the header line of the file

#input.load_samasource_data(tasks_array, f)


stats.t_start = time() #measuring running time of the simulation


for stats.iter in range(0, params.max_num_of_iterations):
			
	if stats.iter % 100 == 0:
		print '*** starting iteration '+str(stats.iter+1)+',  time: '+str(stats.cur_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(stats.total_steps_entered_system)+']'
		utils.print_statistics()			
		
	#if utils.get_num_of_days_passed() > 500:# or (stats.total_backlog / (stats.iter+1)) > 500:
	#	break
		
	if stats.steps_file_ended == 1 and not tasks_array:
		break
		
	input.load_samasource_data(tasks_array, f)
	ready_workers = [x for x in workers_array if x.is_ready() == True]
	algorithm[params.algo_type](tasks_array, ready_workers)
	tasks_array = [x for x in tasks_array if not x.is_fully_scheduled()]
	stats.total_backlog += (stats.total_steps_entered_system - stats.fully_scheduled_steps)
	stats.cur_time += params.time_step

stats.t_end = time()

f.close

print '=== final statistics ==='
print '*** finished iteration '+str(stats.iter+1)+',  time: '+str(stats.cur_time)+\
		'. [full sched: '+str(stats.fully_scheduled_steps)+\
		', comp: '+str(stats.completed_steps)+\
		', total: '+str(stats.total_steps_entered_system)+']'
utils.print_statistics()


if os.path.isfile('y_res.txt') == False:
	thefile = open('y_res.txt', 'a')
	thefile.write("#algo,load(tasks/h),tasks_file,TAT,num_of_tasks,S_TAT,S_num_of_tasks,S_max_days,backlog_avg,utilization,days_passed,runtime,time_step,buf\n")
else:
	thefile = open('y_res.txt', 'a')


thefile.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (\
params.algo_type,\
params.num_of_new_tasks_per_hour,\
options.tasks_input_file,\
round(stats.total_tasks_turnaround_time/stats.total_finished_tasks,2),\
stats.total_finished_tasks,\
round(stats.samasource_tasks_total_tunaround/stats.samasource_tasks_entered,2),\
stats.samasource_tasks_entered,\
params.max_task_turnaround_days,\
round(stats.total_backlog / stats.iter,2),\
round(stats.new_total_work_time/(stats.total_available_work_time_per_day*(utils.get_num_of_days_passed()))/3600,5)*100,\
round(utils.get_num_of_days_passed(),2),\
round(time()-stats.t_start,3),\
params.time_step,\
params.buf))

thefile.close()

