import subprocess
import itertools
import shutil
from pathlib import Path
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--fpt', default=False, action='store_true')
parser.add_argument('--fd_heur', default=False, action='store_true')
args = parser.parse_args()
    
# start all_ouputs file with k values
Path("all_outputs.txt").unlink()
f = open("all_outputs.txt", "a")
f.write("2,3,4,5,6,7,8,9,10\n")
f.close()

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

print("Computing accuracies for each of:")
for exp_type in exp_types:
    for length, sps in combos:
        print("{},{},{}...".format(exp_type, length, sps))
        subprocess.run([
            "python", "process_output.py",
            "acyclic_sc_graph_instances/len{}dem1subpaths{}/truth/graphs.truth".
            format(length, sps),
            "acyclic_sc_graph_instances/len{}dem1subpaths{}/predicted_{}/all_pred.txt".
            format(length, sps, exp_type)], check=True)

def print_np_array_as_latex_table(a):
    print("\\\\\n".join([" & ".join(map(str, line)) for line in a]))


# make latex table from file
data = np.loadtxt("all_outputs.txt", delimiter=",")
data = data.transpose()
print_np_array_as_latex_table(data)
