import re
import os

def read_optim(file_path):
    results = {}

    # 파일 읽기
    with open(file_path, "r") as file:
        content = file.read()

        matches = re.findall(r"^\s*\d+\s+(M|L|A)\s+\*\s+(\d+)", content, re.MULTILINE)

        for match in matches:
            column_name, value = match
            results[column_name] = int(value)
    print(f"M: {results['M']}, L: {results['L']}, A: {results['A']}")
 
# directory_path = "/content/drive/MyDrive/Course/2024\ FALL/ENEE759U/Final_project/output"

# for filename in os.listdir(directory_path):
#     file_path = os.path.join(directory_path, filename)

#     # 파일인지 확인 (디렉터리 제외)
#     if os.path.isfile(file_path):
#         print(f"Processing file: {filename[-22:-4]}")
#         read_optim(file_path)