#from __future__ import division
import params

wasted_workers_time = 0
total_available_work_time = 0
total_work_time = 0
total_skills_requirements_time = 0 #should be the same as total_work_time
fully_scheduled_steps = 0
completed_steps = 0
total_steps_in_system_time = 0
total_steps_entered_system = 0
t_start = 0
t_end = 0
total_waiting_time = 0
cur_time = 0 #in seconds
total_tasks_generated = 0
total_available_work_time_per_day = 0

total_finished_tasks = 0
total_tasks_turnaround_time = 0
samasource_tasks_entered = 0
samasource_tasks_total_tunaround = 0

new_total_work_time = 0
total_backlog = 0
iter = 0
#residual_count = 0
data_files_rows_read = 1	
	
steps_avg_duration_dict = {}
#last_task_id = -1
last_loaded_step_time = 0
