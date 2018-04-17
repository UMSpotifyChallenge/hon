import csv
from os import listdir
import argparse
# from os.path import isfile, join

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, default=".", help="path for testing result folder")
parser.add_argument("--size", type=int, default=0, help="# of unique tracks")
args = parser.parse_args()

files = [f for f in listdir(args.path)]

track_counts = args.size
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

none_count = 0
result_per_pl = []
result_per_pl_prec = []



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
        if rank != -1:
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
        else:
            none_count += 1

    result = []
    result.append(per_pl_top500_count / per_pl_testing_count * 100)
    result.append(per_pl_top01p_count / per_pl_testing_count * 100)
    result.append(per_pl_top02p_count / per_pl_testing_count * 100)
    result.append(per_pl_top05p_count / per_pl_testing_count * 100)
    result.append(per_pl_top10p_count / per_pl_testing_count * 100)

    result_prec = []
    result_prec.append(per_pl_top500_count / float(500) * 100)
    result_prec.append(per_pl_top01p_count / cond_top01p * 100)
    result_prec.append(per_pl_top02p_count / cond_top02p * 100)
    result_prec.append(per_pl_top05p_count / cond_top05p * 100)
    result_prec.append(per_pl_top10p_count / cond_top10p * 100)

    result_per_pl.append(result)

    result_per_pl_prec.append(result_prec)


with open('result.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    overall_result = []
    overall_result.append("#Overall Results: ")
    overall_result.append(top500_count / testing_count * 100)
    overall_result.append(top01p_count / testing_count * 100)
    overall_result.append(top02p_count / testing_count * 100)
    overall_result.append(top05p_count / testing_count * 100)
    overall_result.append(top10p_count / testing_count * 100)
    csvwriter.writerow(overall_result)

    for r in result_per_pl:
        csvwriter.writerow(r)


with open('result_prec.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    for r in result_per_pl_prec:
        csvwriter.writerow(r)

print(none_count)
print(testing_count)

# print(top500_count/testing_count * 100)
# print(top01p_count/testing_count * 100)
# print(top02p_count/testing_count * 100)
# print(top05p_count/testing_count * 100)
# print(top10p_count/testing_count * 100)
