import sys
import os

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

sp = file_path.split('_')[0]
new_file_name = "mirIDupdated_" + file_name

with open(file_name, "r") as f:
    lines = f.readlines()

with open(new_file_name, "w") as f:
    for line in lines:
        #line = '\t'.join(line.split())
        line = line.split("\t")
        line[3] = sp + line[3][3:]
        #f.write("\t".join(line) + "\n")

        f.write("\t".join(line))
