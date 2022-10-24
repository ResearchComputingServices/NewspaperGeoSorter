#!/bin/bash

DEBUG_FLAG=true

# For production run
#YEARS=(2016 2017 2018 2019 2020 2021 2022)
#MONTHS=(January February March April May June July August September October November December)

# For test run
if [DEBUG_FLAG]; then
  YEARS=(2016)
  MONTHS=(August September October November December)
fi

JOB_ARRAY=()

NUM_PROCESSES=10
JOBS_COMPLETED=0
TOTAL_JOBS=0

# Check that exactly one command line argument has been passed
if [ "$#" -ne 3 ]; then
    echo "Please provide an input and output directory"
fi

# assign the input and output directories
UNSORTED_DATA_DIR=$1
SORTED_DATA_DIR=$2
NEWSPAPER_DATA_DIR=$3

#SORTED_DATA_DIR='/home/nickshiell/storage/SortedByState/'

# Clear out the previous sorted data
if [!DEBUG_FLAG]; then
  #echo "Deleteing previous SORTED files"
  #find ${SORTED_DATA_DIR}/States -name *.csv -delete
  #echo "DONE!"

  #echo "Deleteing previous REPORT files"
  #find ${SORTED_DATA_DIR}/Reports -name *.txt -delete
  #echo "DONE!"
fi

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
    if [!DEBUG_FLAG]; then
      python3 ArticleSorter.py ${JOB_ARRAY[$JOBS_COMPLETED]} ${UNSORTED_DATA_DIR} ${SORTED_DATA_DIR} ${NEWSPAPER_DATA_DIR}&
    else
      python3 test.py ${JOB_ARRAY[$JOBS_COMPLETED]} ${UNSORTED_DATA_DIR} ${SORTED_DATA_DIR} ${NEWSPAPER_DATA_DIR}&
    fi
    
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