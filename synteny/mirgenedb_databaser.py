#!/usr/bin/env python3

import re

mature_dict = {}
with open("mammals_mature.fa") as f:
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            mir_id = line[1:].split()[0]
        else:
            mature_dict[mir_id] = line

star_dict = {}
with open("mammals_star.fa") as f:
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            mir_id = line[1:].split()[0]
        else:
            star_dict[mir_id] = line

loop_dict = {}
with open("mammals_loop.fa") as f:
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            mir_id = line[1:].split()[0]
        else:
            loop_dict[mir_id] = line

with open("mammals_mirgenedb_TABLE.txt") as f:
    next(f)
    print(f"mirgenedb_id\tmirbase_id\tfamily\tmature_arm\tseed\tseed_start\tseed_end\tmature_seq\tmature_start\tmature_end\tloop_seq\tloop_start\tloop_end\tstar_seq\tstar_start\tstar_end\tstrand")
    for line in f:
        mirgenedb_id, mirbase_id, family, seed, strand = line.strip().split("\t")
        mature_arm = mature_seq = seed_start = seed_end = mature_start = mature_end = star_seq = star_start = star_end = "NA"

        pattern = re.compile(rf"^{re.escape(mirgenedb_id)}(-P\d+[a-z]?|-v\d+)?_(5p|3p)$")
        mature_matches = [(k, seq) for k, seq in mature_dict.items() if pattern.match(k)]
        if not mature_matches:
            fallback_pattern = re.compile(rf"^{re.escape(mirgenedb_id)}_(5p|3p)$")
            mature_matches = [(k, seq) for k, seq in mature_dict.items() if fallback_pattern.match(k)]

        loop_pattern = re.compile(rf"^{re.escape(mirgenedb_id)}(-P\d+[a-z]?|-v\d+)?_loop$")
        loop_matches = [(k, seq) for k, seq in loop_dict.items() if loop_pattern.match(k)]
        if not loop_matches:
            fallback_pattern = re.compile(rf"^{re.escape(mirgenedb_id)}_loop$")
            loop_matches = [(k, seq) for k, seq in loop_dict.items() if fallback_pattern.match(k)]

        if loop_matches:
            loop_seq = loop_matches[0][1]
        else:
            loop_seq = "NA"

        if len(mature_matches) > 1:
            for k, seq in mature_matches:
                seed_local = seed if seed in seq else seq[1:8]

                if "_5p" in k:
                    mature_seq = seq
                    mature_arm = "5p"
                    mature_start = 1
                    seed_start = 2
                    seed_end = 8
                    mature_end = len(mature_seq)
                    loop_start = mature_end + 1
                    loop_end = loop_start + len(loop_seq) - 1
                    star_start = "NA"
                    star_end = "NA"
                    star_seq = "NA"

                    newline = "\t".join(
                        [mirgenedb_id, mirbase_id, family, mature_arm, seed_local, str(seed_start), str(seed_end), mature_seq,
                         str(mature_start), str(mature_end), loop_seq, str(loop_start), str(loop_end),
                         star_seq, str(star_start), str(star_end), strand])
                    print(newline)

                elif "_3p" in k:
                    mature_seq = seq
                    mature_arm = "3p"
                    mature_start_3p = loop_end + 1
                    seed_start = mature_start_3p + 1
                    seed_end = mature_start_3p + 8
                    mature_end = mature_start_3p + len(mature_seq) - 1
                    loop_start = mature_end + 1
                    loop_end = loop_start + len(loop_seq) - 1
                    star_start = "NA"
                    star_end = "NA"
                    star_seq = "NA"

                    newline = "\t".join(
                        [mirgenedb_id, mirbase_id, family, mature_arm, seed_local, str(seed_start), str(seed_end), mature_seq,
                         str(mature_start_3p), str(mature_end), loop_seq, str(loop_start), str(loop_end),
                         star_seq, str(star_start), str(star_end), strand])
                    print(newline)

        elif len(mature_matches) == 1:
            for mature_ID, mature_seq in mature_matches:
             mature_arm = "5p" if "_5p" in mature_ID else "3p"

            star_seq = "NA"
            if mature_arm == "5p":
                expected_star_key = mature_ID.replace("_5p", "_3p*")
            else:
                expected_star_key = mature_ID.replace("_3p", "_5p*")

            if expected_star_key in star_dict:
                star_seq = star_dict[expected_star_key]
            else:
                star_pattern = re.compile(rf"^{re.escape(mirgenedb_id)}(-P\d+[a-z]?|-v\d+)?_(5p|3p)\*$")
                star_matches = [(k, seq) for k, seq in star_dict.items() if star_pattern.match(k)]
                if not star_matches:
                    simple_star_pattern = re.compile(rf"^{re.escape(mirgenedb_id)}_(5p|3p)\*$")
                    star_matches = [(k, seq) for k, seq in star_dict.items() if simple_star_pattern.match(k)]

            seed_start = seed_end = mature_start = mature_end = loop_start = loop_end = star_start = star_end = "NA"

            # --- COORDINATE CALCULATION ---
            if mature_arm == "5p":
                mature_start = 1
                seed_start = 2
                seed_end = 8
                mature_end = len(mature_seq)
                loop_start = mature_end + 1
                loop_end = loop_start + len(loop_seq) - 1
                star_start = loop_end + 1 if star_seq != "NA" else "NA"
                star_end = star_start + len(star_seq) - 1 if star_seq != "NA" else "NA"
            elif mature_arm == "3p":
                star_start = 1 if star_seq != "NA" else "NA"
                star_end = len(star_seq) if star_seq != "NA" else "NA"
                loop_start = star_end + 1 if star_end != "NA" else 1
                loop_end = loop_start + len(loop_seq) - 1
                mature_start = loop_end + 1
                seed_start = mature_start + 1
                seed_end = mature_start + 8
                mature_end = mature_start + len(mature_seq) - 1

            # --- OUTPUT ---
            newline = "\t".join(
                [mirgenedb_id, mirbase_id, family, mature_arm, seed, str(seed_start), str(seed_end), mature_seq,
                 str(mature_start), str(mature_end), loop_seq, str(loop_start), str(loop_end),
                 star_seq, str(star_start), str(star_end), strand])
            print(newline)