from os import abort
import argparse
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import write_dot
import os
from minimize import minimize_both
def auto_schedule(args):
  G = nx.read_edgelist(
    args.g,
    create_using=nx.DiGraph(),
    nodetype=int,
    data=(('weight', float),)
  )
  critical_path_length = nx.dag_longest_path_length(G, weight=1)
  write_dot(G, 'file.dot')
  print(critical_path_length)
  edges = list(G.edges(data=True))
  #print(edges)
  num_nodes = G.number_of_nodes()
  num_edges = G.number_of_edges()

  minimize_both(args, critical_path_length, edges, num_nodes, num_edges)


parser = argparse.ArgumentParser(description='ELGraphSAGE Training')
parser.add_argument("--alpha", type=float, default=0.1, help='Memory constraint')
#parser.add_argument("--a", type=int, default=4, help='Resource constraint')
parser.add_argument("--beta", type=float, default=0.6, help='Latency constraint')
parser.add_argument("--gamma", type=float, default=0.3, help='Resource constraint')
parser.add_argument('--g', type=str, default='/Users/curiekim/Workspace/ENEE759U/scheduling_benchmarks/rand_DFG_s15_1.edgelist', help='Filename of edgelist data')
args = parser.parse_args()
auto_schedule(args)
