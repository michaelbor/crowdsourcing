#!/bin/bash
	for i in `seq 20 10 180`; do
		echo starting load: $i algo $1
		python main_test.py $i $1
	done



