#!/usr/bin/env python

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
from optparse import OptionParser
import globals
import distr_bins

globals.sama_bins = distr_bins.distr_bins(100,10000000)


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
       
parser.add_option("--buf", dest="buf",type="int", default = 200000,
                  help="Buffer size - limits burst size - max number of tasks can be stored in the tasks_array", metavar="BUF_SIZE")                  

parser.add_option("--time_step", dest="time_step",type="int", default = 600,
                  help="Time step - time between consequitive schedulings", metavar="TIME_STEP")                  

parser.add_option("--gen_workers", dest="new_workers_filename", default = "",
                  help="If this option is used, the program will generate new workers file. No simulation will bee performed.", metavar="new_workers_filename")                  

parser.add_option("--gen_steps", dest="new_steps_filename", default = "",
                  help="If this option is used, the program will generate new steps file. No simulation will bee performed.", metavar="new_steps_filename")                  

parser.add_option("--sim_mode", dest="simulation_mode", default = "sama",
                  help="Simulation mode: sama - for simulation with samasource data, custom - for simulation with syntethic data.", metavar="sama/custom")                  

parser.add_option("--max_days", dest="max_days", type="int", default = 3650,
                  help="Maximum number of days to simulate. ", metavar="sama/custom")                  

parser.add_option("--stats_file", dest="stats_filename", default = "",
                  help="If this option is used, the program will generate new steps file. No simulation will bee performed.", metavar="new_steps_filename")                  


(options, args) = parser.parse_args()

params.num_of_new_tasks_per_hour = options.num_of_new_tasks_per_hour
params.buf = options.buf
params.time_step = options.time_step

max_iters = int(np.ceil(options.max_days * 24 * 3600 / options.time_step))


if options.new_workers_filename != "":
	gen.generate_workers_db(options.new_workers_filename)
	print 'new workers file is generated: '+options.new_workers_filename
	sys.exit()

if options.new_steps_filename != "":
	gen.generate_steps_db(options.new_steps_filename)
	print 'new steps file is generated: '+options.new_steps_filename
	sys.exit()


algorithms = {\
#1:algo.allocate_jobs1, \
1:algo.allocate_jobs_prio, \
2:algo.allocate_jobs_skills_no_split, \
3:algo.allocate_jobs_steps_no_split}

load_data_functions = {\
"sama":input.load_samasource_data, \
"custom":input.generate_and_load_steps_from_db}

scheduling_algo_func = algorithms[options.algo_type]
load_steps_func = load_data_functions[options.simulation_mode]

workers_array = []
tasks_array = []


if options.simulation_mode == "sama":
	input.load_steps_duration(options.avg_steps_duration_file)
	globals.sama_tasks_file = open(options.tasks_input_file, 'r')
	globals.sama_tasks_file.readline() #skip the header line of the file
	if options.stats_filename == "":
		options.stats_filename = "y_stats_sama.txt"
else:
	input.load_steps_db_to_memory(options.tasks_input_file)
	if options.stats_filename == "":
		options.stats_filename = "y_stats_custom.txt"


input.init_workers_from_db(options.workers_file, workers_array)


stats.cur_time = params.time_step
stats.t_start = time() #measuring running time of the simulation


#k=[229,0,77,0,1,0,2,3,0,0,4,0,0,0,0,0,5,6,0,7,8,0,9,0,0,4,0]
#print k
#utils.sort_tasks_two_priorities1(k)
#print k
#sys.exit()

for stats.iter in range(0, max_iters):
			
	if stats.iter % 100 == 0:
		utils.print_statistics()			
		
	if stats.steps_file_ended == 1 and not tasks_array:
		break
		
	load_steps_func(tasks_array)
	ready_workers = [x for x in workers_array if x.is_ready() == True]
	scheduling_algo_func(tasks_array, ready_workers,1)
	scheduling_algo_func(tasks_array, ready_workers,0)
	tasks_array = [x for x in tasks_array if not x.is_completed()]
	stats.total_backlog += (stats.total_steps_entered_system - stats.fully_scheduled_steps)
	stats.cur_time += params.time_step

stats.t_end = time()

if options.simulation_mode == "sama":
	globals.sama_tasks_file.close()

print '=== final statistics ==='
utils.print_statistics()

utils.write_stats_to_file(options)

globals.sama_bins.write_to_file("bins.txt")

