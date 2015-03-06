
from step_class import Step
from task_class import Task



s1 = Step(1, 23.3, 300, [['read',3000],['write',2000],['C',3000]], 15,1)
s2 = Step(2, 23.3, 300, [['read',3000],['write',2000],['C',3000]], 15,4)
s3 = Step(3, 23.3, 300, [['read',3000],['write',2000],['C',3000]], 15,3)
s4 = Step(4, 23.3, 300, [['read',3000],['write',2000],['C',3000]], 15,6)
s5 = Step(5, 23.3, 300, [['read',3000],['write',2000],['C',3000]], 15,2)
s6 = Step(6, 23.3, 300, [['read',3000],['write',2000],['C',3000]], 15,1)

t1 = Task(1, 1000)


print 'array experiment:'


t1.print_task_steps()

t1.add_step(s1)
t1.add_step(s2)
t1.add_step(s3)
t1.add_step(s4)
t1.add_step(s6)
t1.add_step(s5)

t1.print_task_steps()

t1.sort_steps_ordering()
print '===='
t1.print_task_steps()


#print s1.print_step();
#print 'Hello world!!!'
