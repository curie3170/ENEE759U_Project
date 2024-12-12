import os
latency_start = 40  
latency_end = 30    
area = 4            
mode = "memory"     
file_path = "/content/ENEE759U/scheduling_benchmarks/rand_DFG_s50_1.edgelist"
save_dir = "/content/drive/MyDrive/Course/2024_FALL/ENEE759U/Final_project/output/"
file_wo_ext = os.path.splitext(file_path)[0]
file_name_wo_ext = os.path.splitext(os.path.basename(file_path))[0]

commands = []
for latency in range(latency_start, latency_end - 1, -1):  
    command1 = f"python3 /content/drive/MyDrive/Course/2024_FALL/ENEE759U/Final_project/auto_schedule.py --mode {mode} --l {latency} --a {area} --g {file_path}"
    command2 = (f"cd glpk-5.0/examples;./glpsol --cpxlp "
                f"{file_wo_ext}_Memory_min_l_{latency}_a_{area}.lp "
                f"-o {save_dir}{file_name_wo_ext}_Memory_min_l_{latency}_a_{area}.out")
    commands.append(f"{command1}\n{command2}")

with open("/content/drive/MyDrive/Course/2024_FALL/ENEE759U/Final_project/script_diff_latency.sh", "w") as f:
    f.write("\n".join(commands))