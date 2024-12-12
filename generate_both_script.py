import os
commands = []
step = 0.1  # 그리드 간격
file_path = "/content/ENEE759U/scheduling_benchmarks/rand_DFG_s20_1.edgelist"
save_dir = "/content/drive/MyDrive/Course/2024_FALL/ENEE759U/Final_project/output/"
file_wo_ext = os.path.splitext(file_path)[0]
file_name_wo_ext = os.path.splitext(os.path.basename(file_path))[0]

# # alpha, beta
# for alpha in [round(i * step, 2) for i in range(int(1 / step) + 1)]:
#     beta = round(1 - alpha, 2)  # beta는 1 - alpha
#     command1 = f"python3 /content/drive/MyDrive/Course/2024_FALL/ENEE759U/Final_project/auto_schedule_both.py --alpha {alpha} --beta {beta} --g {file_path}"
#     command2 = f"cd glpk-5.0/examples;./glpsol --cpxlp {file_wo_ext}_Both_min_alpha_{alpha}_beta_{beta}.lp -o {save_dir}{file_name_wo_ext}_Both_min_alpha_{alpha}_beta_{beta}.out"
#     commands.append(f"{command1}\n{command2}")

# alpha, beta, gamma
# for alpha in [i * step for i in range(1, int(1/step))]:
#     alpha = round(alpha, 2)
#     for beta in [i * step for i in range(1, int(1/step))]:
#         beta = round(beta, 2)
#         gamma = round(1 - (alpha + beta), 2)
#         if 0 < gamma < 1:
#           print(alpha, beta, gamma)
#           command1 = f"python3 /content/drive/MyDrive/Course/2024_FALL/ENEE759U/Final_project/auto_schedule_both.py --alpha {alpha} --beta {beta} --gamma {gamma} --g {file_path}"
#           command2 = f"cd glpk-5.0/examples;./glpsol --cpxlp {file_wo_ext}_Both_min_alpha_{alpha}_beta_{beta}_gamma_{gamma}.lp -o {save_dir}{file_name_wo_ext}_Both_min_alpha_{alpha}_beta_{beta}_gamma_{gamma}.out"
#           commands.append(f"{command1}\n{command2}")

alpha_list = [0.1, 0.1, 0.1, 0.2, 0.3, 0.3, 0.4, 0.4, 0.5, 0.6, 0.8]
beta_list = [0.1, 0.4, 0.8, 0.4, 0.1, 0.5, 0.1, 0.5, 0.3, 0.2, 0.1]
gamma_list = [0.8, 0.5, 0.1, 0.4, 0.6, 0.2, 0.5, 0.1, 0.2, 0.2, 0.1]

for i in range(11):
  alpha = alpha_list[i]
  beta = beta_list[i]
  gamma = gamma_list[i]
  command1 = f"python3 /content/drive/MyDrive/Course/2024_FALL/ENEE759U/Final_project/auto_schedule_both.py --alpha {alpha} --beta {beta} --gamma {gamma} --g {file_path}"
  command2 = f"cd glpk-5.0/examples;./glpsol --cpxlp {file_wo_ext}_Both_min_alpha_{alpha}_beta_{beta}_gamma_{gamma}.lp -o {save_dir}{file_name_wo_ext}_Both_min_alpha_{alpha}_beta_{beta}_gamma_{gamma}.out"
  commands.append(f"{command1}\n{command2}")

with open("/content/drive/MyDrive/Course/2024_FALL/ENEE759U/Final_project/triple_script.sh", "w") as f:
    f.write("\n".join(commands))


# 0.1 0.1 0.8 o
# 0.1 0.2 0.7
# 0.1 0.3 0.6
# 0.1 0.4 0.5 o
# 0.1 0.5 0.4
# 0.1 0.6 0.3
# 0.1 0.7 0.2
# 0.1 0.8 0.1 o
# 0.2 0.1 0.7
# 0.2 0.2 0.6
# 0.2 0.3 0.5
# 0.2 0.4 0.4 o
# 0.2 0.5 0.3
# 0.2 0.6 0.2
# 0.2 0.7 0.1
# 0.3 0.1 0.6  o
# 0.3 0.2 0.5
# 0.3 0.3 0.4
# 0.3 0.4 0.3
# 0.3 0.5 0.2  o
# 0.3 0.6 0.1
# 0.4 0.1 0.5  o
# 0.4 0.2 0.4
# 0.4 0.3 0.3
# 0.4 0.4 0.2
# 0.4 0.5 0.1  o
# 0.5 0.1 0.4
# 0.5 0.2 0.3
# 0.5 0.3 0.2  o
# 0.5 0.4 0.1
# 0.6 0.1 0.3
# 0.6 0.2 0.2  o
# 0.6 0.3 0.1
# 0.7 0.1 0.2
# 0.7 0.2 0.1 
# 0.8 0.1 0.1 o
