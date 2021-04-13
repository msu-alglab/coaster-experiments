import subprocess
from pathlib import Path
import numpy as np


# the lengths and subpaths we want to run experiments for
# (we will also create no subpath versions)
lengths = [3, 4]
subpaths = [1, 2, 3, 4]

"""
# create data
subprocess.run([
"python", "create_sc_instances.py", "basic_instances/",
"acyclic_sc_graph_instances/", "acyclic_sc_graph_instances", "1",
"False", "0", "100000"
])
for length in lengths:
    for sp in subpaths:
        subprocess.run([
"python", "create_sc_instances.py", "basic_instances/",
"acyclic_sc_graph_instances/", "acyclic_sc_graph_instances", str(length),
"False", str(sp), "100000"
])
"""

# run heuristic on data
for length in lengths:
    for sp in subpaths:
        subprocess.run([
            "python", "../coaster/coaster.py",
            "acyclic_sc_graph_instances/len{}dem1subpaths{}/graphs/sc0.graph".
            format(length, sp),
            "--fd_heuristic"], check=True)

# run on no subpath version
subprocess.run([
    "python", "../coaster/coaster.py",
    "acyclic_sc_graph_instances/len1dem1subpaths0/graphs/sc0.graph",
    "--fd_heuristic"], check=True)

Path("all_outputs.txt").unlink(missing_ok=True)
f = open("all_outputs.txt", "a")
f.write("2,3,4,5,6,7,8,9,10,11,12,13,14,15,16\n")
f.close()
subprocess.run([
    "python", "process_output.py",
    "acyclic_sc_graph_instances/len1dem1subpaths0/truth/graphs.truth",
    "acyclic_sc_graph_instances/len1dem1subpaths0/predicted/pred.txt"],
               check=True)
# process the output
for length in lengths:
    for sp in subpaths:
        print(length, sp)
        subprocess.run([
            "python", "process_output.py",
            "acyclic_sc_graph_instances/len{}dem1subpaths{}/truth/graphs.truth".
            format(length, sp),
            "acyclic_sc_graph_instances/len{}dem1subpaths{}/predicted/pred.txt".
            format(length, sp)], check=True)


def print_np_array_as_latex_table(a):
    print("\\\\\n".join([" & ".join(map(str, line)) for line in a]))


# make latex table from file
data = np.loadtxt("all_outputs.txt", delimiter=",")
data = data.transpose()
print_np_array_as_latex_table(data)
