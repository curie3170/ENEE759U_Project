import os
from pathlib import Path
from print_optimized_vals import read_optim
def minimize_memory(args, critical_path_length, edges, num_nodes, num_edges):
    lines = ['Minimize\n']
    lines.append("  M\n")
    # Activated once
    lines.append("Subject To\n")
    lines.append(f"    lat: L = {args.l}\n")
    # Resources
    for i in range(1, args.l+1):
      terms = " + ".join([f"X{j}_{i}" for j in range(1, num_nodes+1)])
      lines.append(f"    res{i}: {terms} - A <= 0\n")
    lines.append(f"    res: A = {args.a}\n")

    # Schedule
    for i in range(1, num_nodes+1):
      assert critical_path_length <= args.l, "Given latency is smaller than critical path"
      assert args.l <= num_nodes, "Given latency is longer than number of nodes"
      terms = " + ".join([f"X{i}_{j}" for j in range(1, args.l+1)])
      lines.append(f"    sch{i}: {terms} = 1\n")

    # Dependencies
    for i in range(num_edges):
      node1, node2, _ = edges[i]
      node1 += 1
      node2 += 1
      terms1 = " + ".join([f"{j} X{node2}_{j}" for j in range(1, args.l+1)])
      terms2 = " - ".join([f"{j} X{node1}_{j}" for j in range(1, args.l+1)])
      lines.append(f"    dep{node1}_{node2}: {terms1} - {terms2} >= 1\n")

    # Define Memory
    variables = set()
    bounds = set()
    terms = []
    eqns = {}
    for i in range(2, args.l+1): # c
      for j in range(num_edges):
        node1, node2, weight = edges[j]
        node1 += 1
        node2 += 1
        weight = int(weight['weight'])
        for k in range(1, i):
          for l in range(i, args.l+1): # k: node1's clk, l: node2's clk. l> k
            terms.append(f"{weight} Y_{node1}_{k}_{node2}_{l}")
            variables.add(f"Y_{node1}_{k}_{node2}_{l}")
            bounds.add(f"    0 <= Y_{node1}_{k}_{node2}_{l} <= 1 \n")
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}a"] = f"Y_{node1}_{k}_{node2}_{l} - X{node1}_{k} - X{node2}_{l} >= - 1 \n"
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}b"] = f"Y_{node1}_{k}_{node2}_{l} - X{node1}_{k} <= 0 \n"
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}c"] = f"Y_{node1}_{k}_{node2}_{l} - X{node2}_{l} <= 0 \n"

      lines.append(f"    mem{i-1}: {' + '.join(terms)} - M <= 0 \n")
      terms = []
    for key, value in eqns.items():
      lines.append(f"    {key}: {value}")
    # Bounds
    lines.append("Bounds\n")
    for i in range(1, num_nodes+1):
      for j in range(1, args.l+1):
        lines.append(f"    0 <= X{i}_{j} <= 1 \n")
    lines.append(f"    M >= 1\n")
    lines.append(f"    A >= 1\n")
    lines.append(f"    1 <= L <= {num_nodes}\n")
    bounds = list(bounds)

    lines.append(f"{''.join(bounds)}")
    # Integer
    lines.append("Integer\n")
    lines.append("    M ")
    lines.append("    L ")
    lines.append("    A ")
    for i in range(1, num_nodes+1):
      for j in range(1, args.l+1):
        lines.append(f"X{i}_{j} ")
    variables = list(variables)
    lines.append(f"{' '.join(variables)}")
    lines.append(f"\nEnd")

    lp_file = args.g.replace(".edgelist", "")+(f"_Memory_min_l_{args.l}_a_{args.a}.lp")
    with open(lp_file, "w") as file:
      file.writelines(lines)
    out_dir = f"{os.getcwd()}/output"
    parent_dir = Path(os.getcwd()).parent
    if not os.path.exists(out_dir):
      os.makedirs(out_dir)
    os.system(f"cd {parent_dir}/glpk-5.0/examples;./glpsol --cpxlp {lp_file} -o {out_dir}/{os.path.splitext(os.path.basename(lp_file))[0]}.out > {out_dir}/log.txt")
    print(f"Saved a processed file in {lp_file}")
    read_optim(f"{out_dir}/{os.path.splitext(os.path.basename(lp_file))[0]}.out")
    
def minimize_latency(args, critical_path_length, edges, num_nodes, num_edges):
    lines = ['Minimize\n']
    lines.append("  L\n")
    # Activated once
    lines.append("Subject To\n")
    lines.append(f"    mem: M = {args.m}\n")
    # Resources
    for i in range(1, num_nodes+1):
      terms = " + ".join([f"X{j}_{i}" for j in range(1, num_nodes+1)])
      lines.append(f"    res{i}: {terms} - A <= 0\n")
    lines.append(f"    res: A = {args.a}\n")
    # Schedule
    for i in range(1, num_nodes+1):
      terms = " + ".join([f"X{i}_{j}" for j in range(1, num_nodes+1)])
      lines.append(f"    sch{i}: {terms} = 1\n")
    # Dependencies
    for i in range(num_edges):
      node1, node2, _ = edges[i]
      node1 += 1
      node2 += 1
      terms1 = " + ".join([f"{j} X{node2}_{j}" for j in range(1, num_nodes+1)])
      terms2 = " - ".join([f"{j} X{node1}_{j}" for j in range(1, num_nodes+1)])
      lines.append(f"    dep{node1}_{node2}: {terms1} - {terms2} >= 1\n")

    # Define Memory
    variables = set()
    bounds = set()
    terms = []
    eqns = {}
    for i in range(2, args.l+1): # c
      for j in range(num_edges):
        node1, node2, weight = edges[j]
        node1 += 1
        node2 += 1
        weight = int(weight['weight'])
        for k in range(1, i):
          for l in range(i, args.l+1): # k: node1's clk, l: node2's clk. l> k
            terms.append(f"{weight} Y_{node1}_{k}_{node2}_{l}")
            variables.add(f"Y_{node1}_{k}_{node2}_{l}")
            bounds.add(f"    0 <= Y_{node1}_{k}_{node2}_{l} <= 1 \n")
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}a"] = f"Y_{node1}_{k}_{node2}_{l} - X{node1}_{k} - X{node2}_{l} >= - 1 \n"
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}b"] = f"Y_{node1}_{k}_{node2}_{l} - X{node1}_{k} <= 0 \n"
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}c"] = f"Y_{node1}_{k}_{node2}_{l} - X{node2}_{l} <= 0 \n"

      lines.append(f"    mem{i-1}: {' + '.join(terms)} - M <= 0 \n")
      terms = []
    for key, value in eqns.items():
      lines.append(f"    {key}: {value}")

    # Define Latency
    for i in range(1, num_nodes+1):
      terms = " + ".join([f"{j} X{i}_{j}" for j in range(1, num_nodes+1)])
      lines.append(f"    lat{i}: {terms} - L <= 0\n")
      #lines.append(f"    lat{i+num_nodes}: {terms} >= 1\n")
    

    # Bounds
    lines.append("Bounds\n")
    for i in range(1, num_nodes+1):
      for j in range(1, num_nodes+1):
        lines.append(f"    0 <= X{i}_{j} <= 1\n")
    lines.append(f"    M >= 1\n")
    lines.append(f"    A >= 1\n")
    lines.append(f"    1 <= L <= {num_nodes}\n")
    bounds = list(bounds)
    lines.append(f"{''.join(bounds)}")
    # Integer
    lines.append("Integer\n")
    lines.append("    M ")
    lines.append("    L ")
    lines.append("    A ")
    for i in range(1, num_nodes+1):
      for j in range(1, num_nodes+1):
        lines.append(f"X{i}_{j} ")
    variables = list(variables)
    lines.append(f"{' '.join(variables)}")

    lines.append(f"\nEnd")
    lp_file = args.g.replace(".edgelist", "")+(f"_Latency_min_m_{args.m}_a_{args.a}.lp")
    with open(lp_file, "w") as file:
      file.writelines(lines)
    out_dir = f"{os.getcwd()}/output"
    parent_dir = Path(os.getcwd()).parent
    if not os.path.exists(out_dir):
      os.makedirs(out_dir)
    os.system(f"cd {parent_dir}/glpk-5.0/examples;./glpsol --cpxlp {lp_file} -o {out_dir}/{os.path.splitext(os.path.basename(lp_file))[0]}.out > {out_dir}/log.txt")
    print(f"Saved a processed file in {lp_file}")
    read_optim(f"{out_dir}/{os.path.splitext(os.path.basename(lp_file))[0]}.out")
    
def minimize_both(args, critical_path_length, edges, num_nodes, num_edges):
    lines = ['Minimize\n']
    lines.append(f"  {args.alpha} M + {args.beta} L + {args.gamma} A\n")
    # Activated once
    lines.append("Subject To\n")

    # Resources
    for i in range(1, num_nodes+1):
      terms = " + ".join([f"X{j}_{i}" for j in range(1, num_nodes+1)])
      lines.append(f"    res{i}: {terms} -A <= 0 \n") # {args.a}\n")

    # Schedule
    for i in range(1, num_nodes+1):
      #assert critical_path_length <= args.l, "Given latency is smaller than critical path"
      terms = " + ".join([f"X{i}_{j}" for j in range(1, num_nodes+1)])
      lines.append(f"    sch{i}: {terms} = 1\n")

    # Dependencies
    for i in range(num_edges):
      node1, node2, _ = edges[i]
      node1 += 1
      node2 += 1
      terms1 = " + ".join([f"{j} X{node2}_{j}" for j in range(1, num_nodes+1)])
      terms2 = " - ".join([f"{j} X{node1}_{j}" for j in range(1, num_nodes+1)])
      lines.append(f"    dep{node1}_{node2}: {terms1} - {terms2} >= 1\n")

    # Define Memory
    variables = set()
    bounds = set()
    terms = []
    eqns = {}
    for i in range(2, num_nodes+1): # c
      for j in range(num_edges):
        node1, node2, weight = edges[j]
        node1 += 1
        node2 += 1
        weight = weight['weight']
        for k in range(1, i):
          for l in range(i, num_nodes+1): # k: node1's clk, l: node2's clk. l> k
            terms.append(f"{weight} Y_{node1}_{k}_{node2}_{l}")
            variables.add(f"Y_{node1}_{k}_{node2}_{l}")
            bounds.add(f"    0 <= Y_{node1}_{k}_{node2}_{l} <= 1 \n")
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}a"] = f"Y_{node1}_{k}_{node2}_{l} - X{node1}_{k} - X{node2}_{l} >= - 1 \n"
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}b"] = f"Y_{node1}_{k}_{node2}_{l} - X{node1}_{k} <= 0 \n"
            eqns[f"mem_sub{node1}_{k}_{node2}_{l}c"] = f"Y_{node1}_{k}_{node2}_{l} - X{node2}_{l} <= 0 \n"

      lines.append(f"    mem{i-1}: {' + '.join(terms)} - M <= 0 \n")
      terms = []
    for key, value in eqns.items():
      lines.append(f"    {key}: {value}")

    # Define Latency
    for i in range(1, num_nodes+1):
      terms = " + ".join([f"{j} X{i}_{j}" for j in range(1, num_nodes+1)])
      lines.append(f"    lat{i}: {terms} - L <= 0\n")

    # Bounds
    lines.append("Bounds\n")
    for i in range(1, num_nodes+1):
      for j in range(1, num_nodes+1):
        lines.append(f"    0 <= X{i}_{j} <= 1 \n")
    lines.append(f"    M >= 1\n")
    lines.append(f"    A >= 1\n")
    lines.append(f"    1 <= L <= {num_nodes}\n")
    bounds = list(bounds)

    lines.append(f"{''.join(bounds)}")
    # Integer
    lines.append("Integer\n")
    lines.append("    M ")
    lines.append("    L ")
    lines.append("    A ")
    for i in range(1, num_nodes+1):
      for j in range(1, num_nodes+1):
        lines.append(f"X{i}_{j} ")
    variables = list(variables)
    lines.append(f"{' '.join(variables)}")

    lp_file = args.g.replace(".edgelist", "")+(f"_Both_min_alpha_{args.alpha}_beta_{args.beta}_gamma_{args.gamma}.lp")
    with open(lp_file, "w") as file:
      file.writelines(lines)
    out_dir = f"{os.getcwd()}/output"
    parent_dir = Path(os.getcwd()).parent
    if not os.path.exists(out_dir):
      os.makedirs(out_dir)
    os.system(f"cd {parent_dir}/glpk-5.0/examples;./glpsol --cpxlp {lp_file} -o {out_dir}/{os.path.splitext(os.path.basename(lp_file))[0]}.out > {out_dir}/log.txt")
    print(f"Saved a processed file in {lp_file}")
    read_optim(f"{out_dir}/{os.path.splitext(os.path.basename(lp_file))[0]}.out")