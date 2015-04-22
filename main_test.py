from __future__ import division
import numpy as np
import algorithm_greedy as algo
import input_handler as input
import utils
import data_generator as gen
import stats
import params
from time import time


gen.generate_workers_db()

workers_array = []
input.init_workers_from_db("workers_db.txt", workers_array)

utils.print_all_workers(workers_array)

ready_workers = utils.get_ready_workers(workers_array)

utils.print_all_workers(ready_workers)
print len(ready_workers)