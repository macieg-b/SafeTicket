#!/bin/bash

PROCESS_NUM="ps aux | grep server.py | wc -l | bc"

KILL_FIRST_PROCESS="ps axf | \
	grep \" python server.py\" | \
	grep -v grep | \
	awk '{print \"kill -9 \" \$1}' |\
	sh"

KILL_SECOND_PROCESS="ps axf | \
	grep \"/usr/bin/python server.py\" | \
	grep -v grep | \
	awk '{print \"kill -9 \" \$1}' |\
	sh"

ADD_LOG_TO_ARCHIVE="cat nohup.out >> log_archive.log"

REMOVE_LOG_FILE="rm nohup.out"

RM_TEMP="rm \"1\""

count=`eval $PROCESS_NUM`

if [ $count -gt 1 ]; then
	eval $KILL_FIRST_PROCESS
	printf "\nFirst stopped\n"
	eval $KILL_SECOND_PROCESS
	printf "Second stopped\n\n"
	eval $ADD_LOG_TO_ARCHIVE
	eval $REMOVE_LOG_FILE
else
	printf "\n\nServer is not already running\n\n\n"
fi
