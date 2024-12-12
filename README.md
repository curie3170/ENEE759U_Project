# ENEE759U Project

This repository contains resources and examples for the ENEE759U project.

## ⚙️ Environment Setup

Follow the steps below to set up the environment for running the project:

1. **Download and Extract GLPK**  
   Use `wget` to download the GLPK (GNU Linear Programming Kit) and extract it and run example:
   ```
   cd {path_to_workspace}
   wget http://ftp.gnu.org/gnu/glpk/glpk-5.0.tar.gz
   tar -zxvf glpk-5.0.tar.gz
   cd glpk-5.0;./configure
   make
   ```
   Run the glpsol solver with a sample LP file:
   ```
   cd {path_to_workspace}/glpk-5.0/examples;./glpsol --cpxlp plan.lp
   ```

3. **Clone Benchmark Dataset Generation Repository**
   ```
   cd {path_to_workspace}
   git clone https://github.com/Yu-Maryland/ENEE759U.git
   ```
4. **Clone This Repository**
   ```
   cd {path_to_workspace}
   git clone https://github.com/curie3170/ENEE759U_Project
   ```


## 🚀 How to Run
1. **Memory optimization scheduling**  
   Execute the script with the required options:
  	-	--l: Latency constraint
  	-	--a: Area constraint
  	-	--g: Path to the edgelist dataset
   Example: 
   ```
   cd {path_to_workspace}/ENEE759U_Project/
   python auto_schedule.py --l 8 --a 4 --g {path_to_workspace}/ENEE759U/scheduling_benchmarks/rand_DFG_s10_1.edgelist
   ```
2. **Latency optimization scheduling**  
   Execute the script with the required options:
  	-	--m: Memory constraint
  	-	--a: Area constraint
  	-	--g: Path to the edgelist dataset
   Example: 
   ```
   cd {path_to_workspace}/ENEE759U_Project/
   python auto_schedule.py --m 140 --a 4 --g {path_to_workspace}/ENEE759U/scheduling_benchmarks/rand_DFG_s10_1.edgelist
   ```
3. **Linear combination optimization scheduling**  
   The objective function of this mode is `alpha * Memory + beta * Latency + gamma + Area`.
   The parameters `alpha + beta + gamma` must sum to 1. This condition is used to approximately determine the feasible range of constraints before starting the Pareto experiments.

   Execute the script with the required options:
  	-	--alpha: Weight of memory
  	-	--beta: Weight of latency
    - --gamma: Weight of area
  	-	--g: Path to the edgelist dataset
   Example: 
   ```
   cd {path_to_workspace}/ENEE759U_Project/
   python auto_schedule.py --alpha 0.1 --beta 0.6 --gamma 0.3 --g {path_to_workspace}/ENEE759U/scheduling_benchmarks/rand_DFG_s10_1.edgelist
   ```

## ⏰ Scheduled Results  
   - The generated .lp file is saved in the same path as the input data file.  
   - The scheduled results are saved in the directory:  
     `{path_to_workspace}/ENEE759U_Project/output`  

   When the scheduling is executed, the output appears as follows:

   ```
   > python auto_schedule.py --l 7 --a 4 --g {path_to_workspace}/ENEE759U/scheduling_benchmarks/rand_DFG_s10_1.edgelist   

   critical path: 6
   Saved a processed file in {path_to_workspace}/ENEE759U/scheduling_benchmarks/rand_DFG_s10_1_Memory_min_l_7_a_4.lp
   M: 106, L: 7, A: 4
   ```

