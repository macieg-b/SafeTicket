#!/bin/bash

PROCESS_NUM="ps aux | grep server.py | wc -l"

count=`eval $PROCESS_NUM`

if [ $count == "1" ]; then
	nohup python server.py &

	count=`eval $PROCESS_NUM`
	if [ $count == "1" ]; then
		printf "\n\nSomething went wrong! Check script correct and try again\n\n\n"
	else
		printf "\n\nServer start\n\n\n" 	
	fi
else
	printf "\n\nServer is already running\n\n\n"
fi
