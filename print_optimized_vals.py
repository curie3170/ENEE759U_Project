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
 