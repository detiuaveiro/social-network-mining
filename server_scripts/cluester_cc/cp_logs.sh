#!/bin/bash

cc_logs=(dbwritter.log mongo.log neo4j.log pdp.log pep.log postgres.log rabbitmq.log translator.log text_generator.log)

cd ~/PI_2020/logs/

now=$(date)
dir_name=${now// /_}
dir_name=${dir_name//:/_}
mkdir $dir_name

for log in ${cc_logs[@]}; do
	docker cp control_center:twitter/$log $dir_name
	docker exec control_center rm $log
done

tar -czvf $dir_name.tar.gz $dir_name
rm -rf $dir_name
