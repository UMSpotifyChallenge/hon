# computes pagerank of network generated as HON
# Input: HON network file
# Output: PageRank for every node


import networkx as nx
import argparse


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

pr = nx.pagerank(G, alpha=0.85, weight = 'weight', tol=1e-09, max_iter=1000)

RealPR = {}

print('converting pr')

for node in pr:
    fields = node.split('|')
    FirstOrderNode = fields[0]
    if not FirstOrderNode in RealPR:
        RealPR[FirstOrderNode] = 0
    RealPR[FirstOrderNode] += pr[node]

print('writing pr')

nodes = sorted(RealPR.keys(), key=lambda x: RealPR[x], reverse=True)

with open('data/pagerank-{}.csv'.format(args.data), 'w') as f:
    for node in nodes:
        f.write(node + ',' + str(RealPR[node]) + '\n')

print('finished')
