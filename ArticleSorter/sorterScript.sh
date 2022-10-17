#!/bin/bash

# For production run
YEARS=(2016 2017 2018 2019 2020 2021 2022)
MONTHS=(January February March April May June July August September October November December)

# For test run
#YEARS=(2016)
#MONTHS=(August September October November December)

JOB_ARRAY=()

NUM_PROCESSES=10
JOBS_COMPLETED=0
TOTAL_JOBS=0

SORTED_DATA_DIR='/home/nickshiell/storage/SortedByState/'

# Clear out the previous sorted data
echo "Deleteing previous SORTED files"
find ${SORTED_DATA_DIR}/States -name *.csv -delete
echo "DONE!"

echo "Deleteing previous REPORT files"
find ${SORTED_DATA_DIR}/Reports -name *.txt -delete
echo "DONE!"

# Create the jobs array
for year in ${YEARS[@]}; do
  for month in ${MONTHS[@]}; do
    JOB_ARRAY+=("${year},${month}")
    ((TOTAL_JOBS=TOTAL_JOBS+1))
  done
done

NUMBER_OF_JOBS=${#JOB_ARRAY[@]}

# Assign the jobs in batchs, when a batch is complete move onto the next
while [ $JOBS_COMPLETED -lt $TOTAL_JOBS ]
do
  
  for (( i=0; i<$NUM_PROCESSES; i++ )); do
    python3 ArticleSorter.py ${JOB_ARRAY[$JOBS_COMPLETED]} &
    #python3 test.py ${JOB_ARRAY[$JOBS_COMPLETED]} &
    pids[${i}]=$!
    ((JOBS_COMPLETED=JOBS_COMPLETED+1))

    # Break out if we run out of jobs
    if [ $JOBS_COMPLETED -ge $NUMBER_OF_JOBS ]
    then
      i=NUM_PROCESSES+1
    fi

  done
 
  # wait for all pids
  for pid in ${pids[*]}; do
    wait $pid
  done

  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
done