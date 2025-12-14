import glob
import re
import os
import sys

target = sys.argv[1]
pat = re.compile(rf"^>[^-\s]+-{target}\b", re.IGNORECASE)

with open(f"{target}.fa", "w") as out:
    for path in glob.glob("*renamed"):
        header, seq = "", []
        for line in open(path):
            if line.startswith(">"):
                if header and pat.match(header):
                    out.write(header + "".join(seq))
                header, seq = line, []
            else:
                seq.append(line)
        if header and pat.match(header):
            out.write(header + "".join(seq))
