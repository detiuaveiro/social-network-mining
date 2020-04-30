#!/bin/bash

FILE_NAME=size.csv
DELTA_TIME=24h

cd ~/PI_2020/logs/

while true; do
   size=$(df -h --outpu=used --total | tail -n 1)
   now=$(date)

   echo $now, $size >> $FILE_NAME

   sleep $DELTA_TIME
done
