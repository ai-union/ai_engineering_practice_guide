#!/bin/bash

set -e 

# spliting the data into trainning set and testing set
echo spliting 
cat allchina_addr.txt| awk '{$1=""}{$2=""}1'> input.data
# shuffling the input sentences
shuf input.data > shuffled_input
split -l $[ $(wc -l shuffled_input|cut -d" " -f1) * 70 / 100 ] shuffled_input crfdata_
wc -l crfdata_*
mv crfdata_aa train.txt
mv crfdata_ab test.txt
# converting input data
echo converting
./make_crfpp_data.py -i train.txt -o  train.data
./make_crfpp_data.py -i test.txt -o  test.data
# training the model
echo training
time crf_learn -p 30 template train.data model.crf 2>&1 | tee  train.log
# echo testing
# crf_test -m model test.data > output.txt

