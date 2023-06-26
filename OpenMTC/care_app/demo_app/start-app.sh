#!/usr/bin/env bash

# base_path is where the start-app.sh is located
base_path=$(dirname "$(readlink -f "${0}")")

################################################################################
# set app_file
declare -a app_array

# print possibilities of system
echo "[1] Smart Farm Monitoring System"
echo "[2] Air Quality Monitoring System"

while true; do
    read -n 1 -p "Choose the system: " init_choice

    if [ ${init_choice} -lt 3 ] && [ ${init_choice} -gt 0 ]
    then
        echo && break
    else
        echo " Wrong choice. Do it again."
    fi
done

if [ ${init_choice} -eq 1 ]
then 
    app_array=($(find ${base_path} -name "spice-*-final.py"))
else
    app_array=($(find ${base_path} -name "care-*-final.py"))
fi

# app_array=($(find ${base_path} -name "*-final.py"))
array_length=${#app_array[@]}

echo 

# print possibilities
for i in $(seq 1 ${array_length}); do
    path=${app_array[$[${i}-1]]}
    echo "[${i}] $(basename ${path})"
done

# read choice
while true; do
    read -n 1 -p "Choose the app to start: " choice

    [[ ${choice} =~ ^[0-9]+$ ]] && \
        [ ${choice} -gt 0 -a ${choice} -le ${array_length} ] && \
        echo && break

    echo " Wrong choice. Do it again."
done

app_file=${app_array[$[${choice}-1]]}

################################################################################
# run app_file
cd ${base_path}
cd ..
. ../common/prep-env.sh
cd ${base_path}
python3 ${app_file}
