#!/bin/bash

bot_logs=(bot_agent.log)

cd ~/PI_2020/logs/

now=$(date "+%A %B %d %T %y")
dir_name=${now// /_}
dir_name=${dir_name//:/_}
mkdir $dir_name

for log in ${cc_logs[@]}; do
	docker cp bot:twitter/$log $dir_name
	docker exec bot sh -c "echo > $log"
done

tar -czf $dir_name.tar.gz $dir_name
rm -rf $dir_name
