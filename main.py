import numpy as np
import algorithm_greedy as algo
import input_handler as input
import utils
import data_generator as gen
import stats
import params



gen.random_steps()
gen.random_workers()

data_steps = np.genfromtxt('input_steps1.txt', delimiter=', ', \
dtype=[('id','i8'), ('arr_time','f8'), ('task_id','i8'),\
 ('skills','S5000'), ('task_prio','i8'), ('order','i8')])

data_workers = np.genfromtxt('input_workers1.txt', delimiter=', ', \
dtype=[('id','i8'),('skills','S5000'), ('avail_time','i8')])


workers_array = [] 
input.init_workers_from_file(data_workers, workers_array)
#utils.print_all_workers(workers_array)

tasks_array = input.init_steps_from_file(data_steps)
#utils.print_all_tasks(tasks_array)

time = 0


for i in range(0, params.max_num_of_iterations):
	
	if i % 100 == 0:
		print '********* starting iteration '+str(i+1)+',  time: '+str(time)+' *****\n'
	utils.update_steps_status(tasks_array)
	utils.update_workers_status(workers_array)
	if utils.is_all_steps_fully_scheduled(tasks_array):
		print 'All steps are fully scheduled. Stopping simulation'
		break
		
	steps_for_allocation = utils.extract_steps_for_allocation(tasks_array, time)
	#utils.print_steps(steps_for_allocation)
	print len(steps_for_allocation)
	algo.allocate_jobs(steps_for_allocation, workers_array, time)
	#utils.print_steps(steps_for_allocation)
	gen.random_workers()
	input.init_workers_from_file(data_workers, workers_array)
	utils.sort_tasks(tasks_array) #needed since the arr_time of a task may change
	
	time = time + params.time_step


#utils.print_all_tasks(tasks_array)
#utils.print_all_workers(workers_array)
print stats.avg_in_system_time(tasks_array)/stats.avg_work_time(tasks_array)
print stats.wasted_workers_time/stats.avg_work_time(tasks_array)

