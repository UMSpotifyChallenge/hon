"""
plot the results generate by hon/evaluation/evaluation.py

argv[1] = path to results file
"""

import sys
import csv
import matplotlib.pyplot as plt

file = open(sys.argv[1], 'r')
csvreader = csv.reader(file)

prec_02p_l = []
prec_500_l = []
prec_01p_l = []
prec_05p_l = []
prec_10p_l = []

# get a list of each precision result for all tests
for row in csvreader:
    if row[0][0] == "#": # if this is the 'overall results' line
        continue
    prec_500_l.append(row[0])
    prec_01p_l.append(row[1])
    prec_02p_l.append(row[2])
    prec_05p_l.append(row[3])
    prec_10p_l.append(row[4])


prec_500_l = map(float,prec_500_l)
prec_01p_l = map(float,prec_01p_l)
prec_02p_l = map(float,prec_02p_l)
prec_05p_l = map(float,prec_05p_l)
prec_10p_l = map(float,prec_10p_l)

avg_500_prec = sum(prec_500_l)/float(len(prec_500_l))
avg_01p_prec = sum(prec_01p_l)/float(len(prec_01p_l))
avg_02p_prec = sum(prec_02p_l)/float(len(prec_02p_l))
avg_05p_prec = sum(prec_05p_l)/float(len(prec_05p_l))
avg_10p_prec = sum(prec_10p_l)/float(len(prec_10p_l))

print("avg 500 precision = " + str(avg_500_prec))
print("avg 1%  precision = " + str(avg_01p_prec))
print("avg 2%  precision = " + str(avg_02p_prec))
print("avg 5%  precision = " + str(avg_05p_prec))
print("avg 10% precision = " + str(avg_10p_prec))

plt.plot(prec_500_l)
