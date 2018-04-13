# computes pagerank of network generated as HON
# Input: HON network file
# Output: PageRank for every node


import networkx as nx
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, default="data", help="input file name in data/ folder")
parser.add_argument("--test", type=str, default="test", help="test file name in data/ folder")
parser.add_argument("--start", type=int, default=0, help="start index of testing to split works among different servers :)")
parser.add_argument("--stop", type=int, default=99999999, help="stop index of testing to split works among different servers :)")
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
with open("data/{}".format(args.test),'r') as f:
    test_plists = json.loads(f.read()) # list with each item a dict with two keys: 'seed' and 'hidden'

# convert values to strings
for j in test_plists:
    for k in j.keys():
        j[k] = str(j[k])
    
testSetNum = 0
for testSet in test_plists:
    if testSetNum < args.start:
        print('SKIP test set {}'.format(str(testSetNum)))
        testSetNum += 1
        continue
    if testSetNum > args.stop:
        break
        
    print('starting test set {}'.format(str(testSetNum)))

    tempDict = {}
    ## first, need to make a dict for the 'seed tracks' / 'personalization vector'
    ## dict is songID -> personalization value (1)
    for s in testSet["seed"]: # for each seed song ID
        key = s+"|"
        tempDict[key] = 1

    print('converting pr')
    pr = nx.pagerank(G, alpha=0.85, personalization = tempDict, weight = 'weight', tol=1e-07, max_iter=1000)
    print('pr converted')

    RealPR = {}
    for node in pr:
        fields = node.split('|')
        FirstOrderNode = fields[0]
        if not FirstOrderNode in RealPR:
            RealPR[FirstOrderNode] = 0
        RealPR[FirstOrderNode] += pr[node]

    print('writing rank for test set {}'.format(str(testSetNum)))

    nodes = sorted(RealPR.keys(), key=lambda x: RealPR[x], reverse=True)

    result = {}
    for hidden in testSet["hidden"]:
        rank = nodes.index(hidden) if hidden in nodes else -1
        result[rank] = hidden

    with open('data/rank_hidden_tracks-{}-test{}.csv'.format(args.data, testSetNum), 'w') as f:
        for rank in sorted(result):
            node = result[rank]
            f.write(node + ',' + str(rank) + '\n')

    testSetNum += 1
