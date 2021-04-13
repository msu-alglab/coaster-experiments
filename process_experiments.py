import subprocess
from pathlib import Path
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('exp_type',
                help='the experiment type: fpt, fd_heur, or ifd_heur')
args = parser.parse_args()
exp_type = args.exp_type

# the lengths and subpaths we want to run experiments for
# (we will also create no subpath versions)
lengths = [3, 4]
subpaths = [1, 2, 3, 4]

# process the output
Path("all_outputs.txt").unlink()
f = open("all_outputs.txt", "a")
f.write("2,3,4,5,6,7,8,9,10,11,12,13,14,15,16\n")
f.close()
subprocess.run([
    "python", "process_output.py",
    "acyclic_sc_graph_instances/len1dem1subpaths0/truth/graphs.truth",
    "acyclic_sc_graph_instances/len1dem1subpaths0/predicted_{}/pred.txt".format(exp_type)],
               check=True)

for length in lengths:
    for sp in subpaths:
        print(length, sp)
        subprocess.run([
            "python", "process_output.py",
            "acyclic_sc_graph_instances/len{}dem1subpaths{}/truth/graphs.truth".
            format(length, sp),
            "acyclic_sc_graph_instances/len{}dem1subpaths{}/predicted_{}/pred.txt".
            format(length, sp, exp_type)], check=True)


def print_np_array_as_latex_table(a):
    print("\\\\\n".join([" & ".join(map(str, line)) for line in a]))


# make latex table from file
data = np.loadtxt("all_outputs.txt", delimiter=",")
data = data.transpose()
print_np_array_as_latex_table(data)
