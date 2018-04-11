# computes pagerank of network generated as HON
# Input: HON network file
# Output: PageRank for every node


import networkx as nx
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, default="data", help="input file name in data/ folder")
args = parser.parse_args()

G = nx.DiGraph()

print('reading network')

with open('data/network-{}.csv'.format(args.data)) as f:
    for line in f:
        fields = line.strip().split(',')
        eFrom = fields[0]
        eTo = fields[1]
        eWeight = float(fields[2])
        G.add_edge(eFrom, eTo, weight = eWeight)

print('computing pr')

# TODO. personalization....
'''
Will need a loop here to loop over all training set playlists
Each training set playlist should be missing a percentage of its original songs
PageRank will run and the top PageRanked songs will be compared to the missing set

This loop will only handle generating PageRank results. Not evaluating them.
'''
test_plists = []
with open("data/hon_testing_1000.txt",'r') as f:
    test_plists = json.loads(f.read()) # list with each item a dict with two keys: 'seed' and 'hidden'

testSetNum = 0
for testSet in test_plists:

    tempDict = {}
    ## first, need to make a dict for the 'seed tracks' / 'personalization vector'
    ## dict is songID -> personalization value (1)
    for s in testSet["seed"]: # for each seed song ID
        tempDict[s] = 1


    pr = nx.pagerank(G, alpha=0.85, personalization = tempDict, weight = 'weight', tol=1e-09, max_iter=1000)

    RealPR = {}

    print('converting pr')

    for node in pr:
        fields = node.split('|')
        FirstOrderNode = fields[0]
        if not FirstOrderNode in RealPR:
            RealPR[FirstOrderNode] = 0
        RealPR[FirstOrderNode] += pr[node]

    print('writing pr for test set {}'.format(str(testSetNum)))

    nodes = sorted(RealPR.keys(), key=lambda x: RealPR[x], reverse=True)

    with open('data/pagerank-{}-TestSet_{}.csv'.format(args.data, testSetNum), 'w') as f:
        for node in nodes:
            f.write(node + ',' + str(RealPR[node]) + '\n')

    testSetNum += 1
