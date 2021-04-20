import subprocess
import itertools
import shutil
from pathlib import Path
import numpy as np
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--fpt', default=False, action='store_true')
parser.add_argument('--fd_heur', default=False, action='store_true')
args = parser.parse_args()
    
# start all_ouputs file with k values
f = open("runtime_outputs.txt", "w")
f.write("2,3,4,5,6,7,8,9,10\n")
f.close()

# get instances info
instance_counts = defaultdict(int)
with open("instance_counts.txt") as f:
    for line in f:
        key = line.split()[0].strip()
        value = int(line.split()[1].strip())
        instance_counts[key] = value

def get_file_runtimes(f, total, counts, min_, max_):
    rf = open(f, "r")
    for line in rf:
        graphname = line.split()[0].split(".graph")[0]
        runtime = float(line.strip().split()[1])
        total += runtime
        counts += 1
        min_ = min(min_, runtime)
        max_ = max(max_, runtime)
    return total, counts, min_, max_

def get_all_exp_runtimes(dirname):
    runtimes_dir = Path(dirname)
    filenames = list(filter(Path.is_file, runtimes_dir.glob('**/*')))
    total = 0
    counts = 0
    min_ = 100
    max_ = 0
    for f in filenames:
        total, counts, min_, max_ = get_file_runtimes(f, total, counts, min_, max_)
    print("count", counts, "avg", total/counts, "min", min_, "max", max_)
    return counts, total, min_, max_
        
# the lengths and subpaths we want to run experiments for
# (we will also create no subpath versions)
lengths = [3, 4]
subpaths = [1, 2, 3, 4]
combos = list(itertools.product(lengths, subpaths))
# the experiment types we want to run
exp_types = []
if args.fpt:
    exp_types += ["fpt"]
if args.fd_heur:
    exp_types += ["fd_heur"]

print("Computing runtimes for each of:")
for exp_type in exp_types:
    overall_min = 100
    overall_max = 0
    overall_counts = 0
    overall_total = 0
    for length, sps in combos:
        print("{},{},{}...".format(exp_type, length, sps))
        runtimes_dir = "acyclic_sc_graph_instances/len{}dem1subpaths{}/runtimes_{}/".format(length, sps, exp_type)
        counts, total, min_, max_ = get_all_exp_runtimes(runtimes_dir)
        overall_min = min(min_, overall_min)
        overall_max = max(max_, overall_max)
        overall_counts += counts
        overall_total += total
    print("\noverall:")
    print("count", overall_counts, "avg", overall_total/overall_counts, "min", overall_min, "max", overall_max)
    

def print_np_array_as_latex_table(a):
    print("\\\\\n".join([" & ".join(map(str, line)) for line in a]))


# make latex table from file
data = np.loadtxt("runtime_outputs.txt", delimiter=",")
data = data.transpose()
print_np_array_as_latex_table(data)
