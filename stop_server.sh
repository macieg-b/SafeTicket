#!/bin/bash

PROCESS_NUM=$(ps aux | grep server.py | wc -l)

KILL_FIRST_PROCESS=$(ps axf | \
	grep " python server.py" | \
	grep -v grep | \
	awk '{print "kill -9 " $1}' |\
	sh)
KILL_SECOND_PROCESS=$(ps axf | \
	grep "/usr/bin/python server.py" | \
	grep -v grep | \
	awk '{print "kill -9 " $1}' |\
	sh)

if [ $PROCESS_NUM > 1 ]; then
	$KILL_FIRST_PROCESS
	echo "First stopped"
	$KILL_SECOND_PROCESS
	echo "Second stopped"
else
	echo "Server is not already running"
fi
