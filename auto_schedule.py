from os import abort
import argparse
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import write_dot
import os
from minimize import minimize_memory, minimize_latency, minimize_both
def auto_schedule(args):

  G = nx.read_edgelist(
    args.g,
    create_using=nx.DiGraph(), 
    nodetype=int,               
    data=(('weight', float),)  
  )

  critical_path_length = nx.dag_longest_path_length(G, weight=1)
  edges = list(G.edges(data=True))
  num_nodes = G.number_of_nodes()
  num_edges = G.number_of_edges()

  if args.l > 0 and args.m == 0 and args.a > 0: # Minimize Memory
    minimize_memory(args, critical_path_length, edges, num_nodes, num_edges)

  elif args.m > 0 and args.l == 0 and args.a > 0:# Minimize Latency
    minimize_latency(args, critical_path_length, edges, num_nodes, num_edges)
  
  elif args.l == 0 and args.m == 0 and args.a ==0: # Minimize alpha* M + beta * Latency + gamma * Area
    minimize_both(args, critical_path_length, edges, num_nodes, num_edges)
  else:
    print("Given arguments are invalid.")


parser = argparse.ArgumentParser(description='ELGraphSAGE Training')
parser.add_argument("--mode", type=str, default='latency', choices=['latency', 'memory'])
parser.add_argument("--l", type=int, default=0, help='Latency constraint')
parser.add_argument("--a", type=int, default=0, help='Resource constraint')
parser.add_argument("--m", type=int, default=0, help='Memory constraint')
parser.add_argument('--g', type=str, default='/Users/curiekim/Workspace/ENEE759U/scheduling_benchmarks/rand_DFG_s10_1.edgelist', help='Filename of edgelist data')
parser.add_argument("--alpha", type=float, default=0.1, help='Memory weight')
parser.add_argument("--beta", type=float, default=0.6, help='Latency weight')
parser.add_argument("--gamma", type=float, default=0.3, help='Resource weight')
args = parser.parse_args()
auto_schedule(args)
