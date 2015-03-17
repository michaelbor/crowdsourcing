import numpy as np
import algorithm_greedy as algo
import input_handler as input
import utils
import data_generator as gen


total_num_of_steps = 200
total_num_of_tasks = 40
gen.random_steps(total_num_of_steps,total_num_of_tasks)

data_steps = np.genfromtxt('input_steps1.txt', delimiter=', ', \
dtype=[('id','i8'), ('arr_time','f8'), ('task_id','i8'),\
 ('skills','S5000'), ('task_prio','i8'), ('order','i8')])

data_workers = np.genfromtxt('input_workers.txt', delimiter=', ', \
dtype=[('id','i8'),('skills','S5000'), ('avail_time','i8')])


workers_array = [] 
input.init_workers_from_file(data_workers, workers_array)
utils.print_all_workers(workers_array)

tasks_array = input.init_steps_from_file(data_steps)
utils.print_all_tasks(tasks_array)

time = 0
time_step = 1000

num_of_iterations = 50

for i in range(0,num_of_iterations):
	
	print '********* starting iteration '+str(i+1)+',  time: '+str(time)+' **********\n'
	utils.update_steps_status(time_step, tasks_array)
	utils.update_workers_status(time_step, workers_array)
	steps_for_allocation = utils.extract_steps_for_allocation(tasks_array)
	utils.print_steps_for_allocation(steps_for_allocation)
	algo.allocate_jobs(steps_for_allocation, workers_array)
	input.init_workers_from_file(data_workers, workers_array)

	time = time + time_step


utils.print_all_tasks(tasks_array)
utils.print_all_workers(workers_array)

