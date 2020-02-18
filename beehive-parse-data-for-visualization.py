#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:32:19 2020

@author: davidnelson

This code attempts to adapt the following tutorial from The Programming
Historian to the Beehive data set.
https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python
"""

# step 0: drop index data DONE
# step 1: drop empty cross-references
# step 2: drop cross references to entries that have not yet been annotated
# step 3: create a regularized spreadsheet of topic and cross-references
# step 3.5: make everything lowercase
# step 4: create a match category for numerical entries (done)
# step 5: separate out match data and item tags (done)
# step 6: create target matches from cross reference data
# so if you have Topic: Apples, Xref: Tree|Fruit|Eve
# place each cross reference on its own line with the topic as source
# and the cross reference as target
# question: are we looking up id tags (which ARE unique) or topic/match data
# (assumed unique)?
# For use with networkx, we need a list of nodes and a list of edges
# the CSV of data and item tags are the nodes, the other CSV are the edges

import csv
import re
import networkx as nx
from operator import itemgetter
from networkx.algorithms import community


def find_numbers(entry):
    '''
    This function will determine if string input contains numbers or not.
    '''
    return any(char.isdigit() for char in entry)


with open('data/beehive-data-network.csv', 'r') as ip, open(
        'beehive-keys.csv', 'w') as op:
    reader = csv.DictReader(ip)
    fields = ['topic', 'item']
    writer = csv.DictWriter(op, fieldnames=fields)
    writer.writeheader()
    for row in reader:
        entry = row['entry']
        topic = row['topic']
        item = row['item']
        if find_numbers(entry) is True:
            match = f'{entry} [{topic}]'
            writer.writerow({'topic': match.lower(), 'item': item})
        else:
            writer.writerow({'topic': topic.lower(), 'item': item})

keys = {}
beehive_topics = []
with open('beehive-keys.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        keys.update({row['item']: row['topic']})
        beehive_topics.append(row['topic'])

# load corrections for idiosyncratic xref data
corrections = {}
with open('data/alpha-corrections.csv', 'r') as ip:
    corrections_reader = csv.DictReader(ip)
    for row in corrections_reader:
        corrections.update({row['input']: row['match']})

with open('data/beehive-data-network.csv', 'r') as ip, open(
        'beehive-edges.csv', 'w') as op:
    reader = csv.DictReader(ip)
    fields = ['source', 'target']
    writer = csv.DictWriter(op, fieldnames=fields)
    writer.writeheader()
    for row in reader:
        entry = row['entry'].lower()
        topic = row['topic'].lower()
        xref = row['xref']
        if find_numbers(entry) is True:
            topic = f'{entry} [{topic}]'
        if xref != '':  # we don't want blank cross-references
            if '|' in xref:
                xref_list = xref.split('|')
                for i in xref_list:
                    if find_numbers(i) is True:
                        xref_num = re.search(r'\d+', i).group()
                        if int(xref_num) < 497:  # last numerical entry for now
                            writer.writerow(
                                    {'source': topic, 'target': i.lower()})
                    elif i in corrections:
                        corrector = corrections[i]
                        correction = keys[corrector]
                        writer.writerow(
                                {'source': topic, 'target': correction})
                    elif i.lower() in beehive_topics:
                        writer.writerow(
                                {'source': topic, 'target': i.lower()})
                    else:
                        print(f'No match for {i}.')
            else:
                if find_numbers(xref) is True:
                    xref_num = re.search(r'\d+', xref).group()
                    if int(xref_num) < 497:
                        writer.writerow(
                                {'source': topic, 'target': xref.lower()})
                elif xref in corrections:
                    corrector = corrections[xref]
                    correction = keys[corrector]
                    writer.writerow({'source': topic, 'target': correction})
                elif xref.lower() in beehive_topics:
                    writer.writerow({'source': topic, 'target': xref.lower()})
                else:
                    print(f'No match for {xref}')

with open('beehive-edges.csv', 'r') as edgecsv:
    edgereader = csv.reader(edgecsv)
    edges = [tuple(e) for e in edgereader][1:]

nodes_list = []
for e in edges:
    for i in e:
        nodes_list.append(i)

nodes = set(nodes_list)

print(len(nodes))
print(len(edges))

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

print(nx.info(G))

density = nx.density(G)
print(density)

necessity_pocket_path = nx.shortest_path(G,
                                         source='necessity', target='pocket')
print('Shortest path from "Necessity" to "Pocket":', necessity_pocket_path)

# components = nx.connected_components(G)
# largest_component = max(components, key=len)
# subgraph = G.subgraph(largest_component)
# diameter = nx.diameter(subgraph)
# print('Network diameter of largest component:', diameter)

# nx.write_gexf(subgraph, 'beehive-sub.gexf')

triadic_closure = nx.transitivity(G)
print('Triadic closure:', triadic_closure)

degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')
print(G.nodes['poverty'])

sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)

print('Top 20 nodes by degree:')
for d in sorted_degree[:20]:
    print(d)

betweenness_dict = nx.betweenness_centrality(G)
eigenvector_dict = nx.eigenvector_centrality(G)

nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')

sorted_betweenness = sorted(
        betweenness_dict.items(), key=itemgetter(1), reverse=True)

print('Top 20 nodes by betweeness centrality:')
for b in sorted_betweenness[:20]:
    print(b)

sorted_eigenvector = sorted(
        eigenvector_dict.items(), key=itemgetter(1), reverse=True)

print('Top 20 nodes by eigenvector centrality:')
for e in sorted_eigenvector[:20]:
    print(e)

# First get the top 20 nodes by betweenness as a list
top_betweenness = sorted_betweenness[:20]

# Then find and print their degree
for tb in top_betweenness:  # Loop through top_betweenness
    degree = degree_dict[tb[0]]
    print("Name:", tb[0], "| Betweenness Centrality:", tb[1], "| Degree:", degree)

communities = community.greedy_modularity_communities(G)

modularity_dict = {}
for i, c in enumerate(communities):
    for name in c:
        modularity_dict[name] = i

nx.set_node_attributes(G, modularity_dict, 'modularity')

class0 = [n for n in G.nodes() if G.nodes[n]['modularity'] == 0]
class0_eigenvector = {n: G.nodes[n]['eigenvector'] for n in class0}
class0_sorted_by_eigenvector = sorted(
        class0_eigenvector.items(), key=itemgetter(1), reverse=True)

print('Modularity class 0 sorted by eigenvector centrality:')
for node in class0_sorted_by_eigenvector[:5]:
    print('Name:', node[0], '| Eigenvector Centrality:', node[1])

for i, c in enumerate(communities):
    if len(c) > 2:
        print(f'Class {str(i)}: {list(c)}')

nx.write_gexf(G, 'beehive-network.gexf')
