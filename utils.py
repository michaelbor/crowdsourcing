from __future__ import division
import stats
import params
from time import time
import sys


def parse_skills_steps(skills_string):
	k = skills_string.translate(None,'[]')
	k = k.split(',')
	k = map(int,k)
	k=[[k[2*i],k[2*i+1]] for i in range(int(len(k)/2))]
	return k
	

def print_all_tasks(tasks_array):
	count = 1
	print "printing all tasks:"
	print "---------------------------------------------"
	for i in tasks_array:
		print str(count)+") task_id: "+str(i.id)
		i.print_task_steps()
		print ''
		count += 1
		
	print "---------------------------------------------\n"


def print_all_workers(workers_array):
	print "printing all workers:"
	print "---------------------------------------------"
	for i in workers_array:
		print 'worker: '+i.print_worker()
		
	print "---------------------------------------------\n"




def print_steps(steps):
	print "printing steps:"
	print "---------------------------------------------"
	for i in steps:
		print i.print_step()
		
	print "---------------------------------------------\n"



def get_step_status(task, step):
	if step.isLocked == True:
		return 1
	elif step.isCompleted == True:
		return 2
	else:
		if step.isFullyScheduled == True:
		 	if step.finish_time <= stats.cur_time: #step.timeToFinish == 0:
				step.isCompleted = True
				stats.completed_steps += 1
				unlock_next_steps(step, task.steps_array)
			
			return 2
			
		else:
			if step.arr_time <= stats.cur_time:
				return 0
			else:
				return 1
		


	
def extract_steps_for_allocation_and_update_steps(tasks_array):
	steps_for_allocation=[]
	for task in tasks_array:
		for step in task.steps_array:
			if step.isLocked == True:				
				break
			elif step.isCompleted == True:
				continue
			else:
				if step.isFullyScheduled == True and step.finish_time <= stats.cur_time: #step.timeToFinish == 0:
					step.isCompleted = True
					stats.completed_steps += 1
					unlock_next_steps(step, task.steps_array)
				elif step.isFullyScheduled == False and step.arr_time <= stats.cur_time:
					if step.waiting_time == 0:
						step.waiting_time = stats.cur_time - step.arr_time
					steps_for_allocation.extend([step])
						
	return steps_for_allocation	
	
	
	
def unlock_next_steps(cur_step, steps_array):
	idx = steps_array.index(cur_step)
	if idx == len(steps_array) - 1:
		return
	if cur_step.order < steps_array[idx+1].order:
		order_of_first = steps_array[idx+1].order	
		for i in range(idx+1, len(steps_array)):
			if steps_array[i].order == order_of_first:
				steps_array[i].isLocked = False
				#if steps_array[i].task_id == '524326fc2d7bef2278006801':
				#	print 'task id: '+str(steps_array[i].task_id)+' ordinal: '+str(steps_array[i].order)+' UNLOCKED at time: '+str(stats.cur_time)

			else:
				break
	



def is_all_steps_fully_scheduled(tasks_array):

	if stats.fully_scheduled_steps == params.num_of_steps:
		return True
	else:
		return False
	
	
		
def get_num_of_days_passed():
	return (stats.cur_time)/3600/24
	
	
def print_statistics():
	print '--------- statistics -----------------------------'
	if stats.completed_steps > 0 and stats.new_total_work_time > 0 and stats.fully_scheduled_steps > 0:
		print 'avg backlogged steps: '+str(round(stats.total_backlog / stats.iter,2))
	
	if stats.total_finished_tasks > 0 and stats.total_tasks_turnaround_time > 0:
		print 'avg task turnaround time: ' + \
	 	str(round(stats.total_tasks_turnaround_time/stats.total_finished_tasks,2))+' sec   completed tasks: '+str(stats.total_finished_tasks)
	
	if stats.samasource_tasks_entered > 0 and stats.samasource_tasks_total_tunaround > 0:
		print 'avg SAMASOURCE task turnaround time: ' + \
	 	str(round(stats.samasource_tasks_total_tunaround/stats.samasource_tasks_entered,2))+\
	 	' sec   evaluated tasks: '+str(stats.samasource_tasks_entered)+\
	 	' with at most '+str(params.max_task_turnaround_days)+' days'
	
	if stats.total_available_work_time_per_day > 0:
		print 'days passed: '+str(round(get_num_of_days_passed(),2))
		print 'workers utilization: ' + \
		str(round(stats.new_total_work_time/\
		(stats.total_available_work_time_per_day*(get_num_of_days_passed()))/3600,5)*100)+'%'
		str(round(stats.new_total_work_time/get_num_of_days_passed()))
	
	print 'running time: '+str(round(time()-stats.t_start,3))+' sec'
	print '--------------------------------------------------\n'	

	
def get_local_time_in_hours(timezone):
	#we assume that the current time is according to timezone 0
	return (stats.cur_time/3600 + timezone)%24

def get_time_in_hours(timezone, t):
	#we assume that the current time is according to timezone 0
	return (t/3600 + timezone)%24


def prepare_submission_at(str_from_file):
	ret = str_from_file.split('.')[0]
	return ret
			


	