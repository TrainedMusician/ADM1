#!/usr/bin/env bash
machine_type=${1}
dbms=${2}
scale_factor=${3}

[[ -z "${machine_type}" ]] && { echo "No machine type specified" ; exit 1; }
[[ -z "${dbms}" ]] && { echo "No DBMS specified" ; exit 1; }
[[ -z "${scale_factor}" ]] && { echo "No scale factor specified" ; exit 1; }

[[ ! -f "results/${machine_type}/$dbms/SF-${scale_factor}/q1.out" ]] && { echo 'This combination does not exist'; exit 1; }

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23;do
  answers/cmpq.pl $i answers/query_outputs/q${i}.out results/${machine_type}/$dbms/SF-${scale_factor}/q${i}.out;
done
