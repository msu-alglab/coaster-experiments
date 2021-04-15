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
Path("runtime_outputs.txt").unlink()
f = open("all_outputs.txt", "a")
f.write("2,3,4,5,6,7,8,9,10\n")
f.close()

def get_file_runtimes(f, total_counts, min_, max_):
    pass

def get_all_exp_runtimes(dirname):
    runtimes_dir = Path(dirname)
    filenames = list(filter(Path.is_file, runtimes_dir.glob('**/*')))
    total = defaultdict(int)
    counts = defaultdict(int)
    min_ = defaultdict(float)
    max = defaultdict(float)
    for f in filenames:
        get_file_runtimes(f, total, counts, min_, max_)
        
# the lengths and subpaths we want to run experiments for
# (we will also create no subpath versions)
lengths = [4]
subpaths = [4]
combos = list(itertools.product(lengths, subpaths))
# the experiment types we want to run
exp_types = []
if args.fpt:
    exp_types += ["fpt"]
if args.fd_heur:
    exp_types += ["fd_heur"]

print("Computing runtimes for each of:")
for exp_type in exp_types:
    if exp_type == "fpt":
        dirname = "run_fpt"
    elif exp_name == "fd_heur":
        dirname = "run_heuristic"
    dirname += "_out"
    for length, sps in combos:
        print("{},{},{}...".format(exp_type, length, sps))
        runtimes_dir = "acyclic_sc_graph_instances/len{}dem1subpaths{}/runtimes_{}/".\
    format(length, sps, exp_type)
        get_all_exp_runtimes(runtimes_dirname)

def print_np_array_as_latex_table(a):
    print("\\\\\n".join([" & ".join(map(str, line)) for line in a]))


# make latex table from file
data = np.loadtxt("runtime_outputs.txt", delimiter=",")
data = data.transpose()
print_np_array_as_latex_table(data)
