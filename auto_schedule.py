from os import abort
import argparse
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import write_dot
import os
from minimize import minimize_memory, minimize_latency
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
  num_nodes = G.number_of_nodes()
  num_edges = G.number_of_edges()

  if args.mode == 'memory': # Minimize Memory
    minimize_memory(args, critical_path_length, edges, num_nodes, num_edges)

  elif args.mode == 'latency': # Minimize Latency
    minimize_latency(args, critical_path_length, edges, num_nodes, num_edges)


parser = argparse.ArgumentParser(description='ELGraphSAGE Training')
parser.add_argument("--mode", type=str, default='latency', choices=['latency', 'memory'])
parser.add_argument("--l", type=int, default=10, help='Latency constraint')
parser.add_argument("--a", type=int, default=4, help='Resource constraint')
parser.add_argument("--m", type=int, default=90, help='Memory constraint')
parser.add_argument('--g', type=str, default='/content/ENEE759U/scheduling_benchmarks/rand_DFG_s10_1.edgelist', help='Filename of edgelist data')
args = parser.parse_args()
auto_schedule(args)
