#!/bin/bash

PROCESS_NUM=$(ps aux | grep server.py | wc -l)

if [ $PROCESS_NUM = 1 ]; then
	nohup python server.py &
else
	echo "Server is already running"
fi
