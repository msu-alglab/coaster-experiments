import subprocess
from collections import defaultdict
import shutil
from pathlib import Path
import numpy as np
import argparse
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('--fpt', default=False, action='store_true')
parser.add_argument('--fd_heur', default=False, action='store_true')
args = parser.parse_args()

def get_pred_filenum(filename):
    return int(filename.split(".txt")[0].split("{}/pred".format(exp_type))[1])
    

# the lengths and subpaths we want to run experiments for
# (we will also create no subpath versions)
lengths = [3, 4]
subpaths = [1, 2, 3, 4]
combos = list(itertools.product(lengths, subpaths))
combos = [(1, 0)] + combos  # for no subpath experiment
# the experiment types we want to run
exp_types = []
if args.fpt:
    exp_types += ["fpt"]
if args.fd_heur:
    exp_types += ["fd_heur"]

# dict to store counts of completed instances
graphnames = defaultdict(int)

# for every experiment, copy all individual pred files into one single file
print("combining individual pred files for each of:")
for exp_type in exp_types:
    for length, sps in combos:
        print("{},{},{}...".format(exp_type, length, sps))
        pred_dir = Path("acyclic_sc_graph_instances/len{}dem1subpaths{}/predicted_{}"
                .format(length, sps, exp_type))
        filenames = list(filter(Path.is_file, pred_dir.glob('**/pred*')))
        filenames = [str(f) for f in filenames]
        filenames.sort(key=get_pred_filenum)
        destination = open("acyclic_sc_graph_instances/len{}dem1subpaths{}/predicted_{}/all_pred.txt".format(length,
                    sps, exp_type), "w")
        for f in filenames:
            shutil.copyfileobj(open(f, "r"), destination)
        for filename in filenames:
            with open(filename, "r") as f:
                for line in f:
                    if line[0] == "#":
                        name = line.split("name = ")[1].split(".graph")[0]
                        graphnames[name] += 1
        destination.close()

with open("instance_counts.txt", "w") as f:
    for key in graphnames.keys():
        f.write("{} {}\n".format(key, graphnames[key]))
