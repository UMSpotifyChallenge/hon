import csv
from os import listdir
# from os.path import isfile, join

files = [f for f in listdir(".")]

track_counts = 248572
cond_top01p = track_counts * 0.01
cond_top02p = track_counts * 0.025
cond_top05p = track_counts * 0.05
cond_top10p = track_counts * 0.10

testing_count = 0.0
top500_count = 0
top01p_count = 0
top02p_count = 0
top05p_count = 0
top10p_count = 0

result_per_pl = []



for path in files:
    if path.endswith(".csv") == False:
        continue

    file = open(path, 'r')
    csvreader = csv.reader(file)

    per_pl_testing_count = 0.0
    per_pl_top500_count = 0
    per_pl_top01p_count = 0
    per_pl_top02p_count = 0
    per_pl_top05p_count = 0
    per_pl_top10p_count = 0

    for row in csvreader:
        testing_count += 1
        per_pl_testing_count += 1

        rank = int(row[1])
        if rank < 500:
            top500_count += 1
            per_pl_top500_count += 1
        if rank < cond_top01p:
            top01p_count += 1
            per_pl_top01p_count += 1
        if rank < cond_top02p:
            top02p_count += 1
            per_pl_top02p_count += 1
        if rank < cond_top05p:
            top05p_count += 1
            per_pl_top05p_count += 1
        if rank < cond_top10p:
            top10p_count += 1
            per_pl_top10p_count += 1

    result = []
    result.append(per_pl_top500_count / per_pl_testing_count * 100)
    result.append(per_pl_top01p_count / per_pl_testing_count * 100)
    result.append(per_pl_top02p_count / per_pl_testing_count * 100)
    result.append(per_pl_top05p_count / per_pl_testing_count * 100)
    result.append(per_pl_top10p_count / per_pl_testing_count * 100)

    result_per_pl.append(result)


with open('result.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    overall_result = []
    overall_result.append(top500_count / testing_count * 100)
    overall_result.append(top01p_count / testing_count * 100)
    overall_result.append(top02p_count / testing_count * 100)
    overall_result.append(top05p_count / testing_count * 100)
    overall_result.append(top10p_count / testing_count * 100)
    csvwriter.writerow(overall_result)

    for r in result_per_pl:
        csvwriter.writerow(r)

# print(top500_count/testing_count * 100)
# print(top01p_count/testing_count * 100)
# print(top02p_count/testing_count * 100)
# print(top05p_count/testing_count * 100)
# print(top10p_count/testing_count * 100)
