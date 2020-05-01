#!/bin/bash

# TODO -> THIS CAN BE AUTOMATIC TOO 
logs=(dbwritter.log mongo.log neo4j.log pdp.log pep.log postgres.log rabbitmq.log translator.log \ 
text_generator.log bot_agent.log rabbit_messaging.log)

files_names=$(ls | grep tar.gz | cut -d "_" -f1-3 | sort -u | grep -vP '.*_.*_.{2}.tar.gz')

for file_name in $files_names; do
   mkdir $file_name

   current_files_to_merge=$(ls | grep $file_name | grep tar.gz)
   echo ${current_files_to_merge}
   for current_name in $current_files_to_merge; do
      tar -xzf $current_name
   done

   dir_names=$(ls | grep $file_name | grep -v tar.gz | grep -v $file_name$)
   for log in ${logs[@]}; do
      current_logs=()
      
      for dir in $dir_names; do
         current_logs=(${current_logs[@]} $dir/$log)
      done
      
      cat ${current_logs[@]} > $file_name/$log 2>/dev/null
      # rm -rf $current_name
   done

   tar -czf $file_name.tar.gz $file_name
   rm -rf $file_name
   rm -rf $dir_names
done
