from collections import defaultdict
import shutil
from pathlib import Path
import numpy as np
import argparse
import itertools


NUM_EXTRA_COLS = 4


def get_pred_filenum(filename):
    return int(filename.split(".txt")[0].split("{}/pred".format(exp_type))[1])


def print_as_latex_table(a, num_exps):
    print("\hline")
    for i, row in enumerate(a):
        print(" & ".join(map(str, row)) + "\\\\")
        if (i + 1) % num_exps == 0:
            print("\hline")

def get_next_truth(f):
    header = f.readline()
    graph_id = header.split("= ")[2].split(".")[0]
    newline = f.readline()
    weight_paths = []
    while newline != "" and newline[0] != "#":
        weight_paths.append([int(x) for x in newline.split()])
        last_pos = f.tell()
        newline = f.readline()
    f.seek(last_pos)
    weight_paths.sort()
    weights = []
    paths = []
    for wp in weight_paths:
        weights.append(wp[0])
        paths.append(wp[1:])
    return graph_id, paths, weights

def get_corresp_truth(f, graph_id):
    # print("Trying to find corresponding truth")
    # print("graph id is", graph_id)
    header = f.readline()
    this_graph_id = header.split("= ")[2].split(".")[0]
    # print("this graph id is", this_graph_id)
    while this_graph_id != graph_id:
        newline = f.readline()
        if newline[0] == "#":
            this_graph_id = newline.split("= ")[2].split(".")[0]
    last_pos = f.tell()
    newline = f.readline()
    weight_paths = []
    while newline != "" and newline[0] != "#":
        weight_paths.append([int(x) for x in newline.split()])
        last_pos = f.tell()
        newline = f.readline()
    f.seek(last_pos)
    weight_paths.sort()
    weights = []
    paths = []
    for wp in weight_paths:
        weights.append(wp[0])
        paths.append(wp[1:])
    return paths, weights


def get_next_predicted(f):
    header = f.readline()
    # print(header)
    graph_id = header.split("= ")[2].split(".")[0]
    last_pos = f.tell()
    newline = f.readline()
    weight_paths = []
    while newline != "" and newline[0] != "#":
        weight_paths.append([int(x) for x in newline.split()])
        last_pos = f.tell()
        newline = f.readline()
    f.seek(last_pos)
    weight_paths.sort()
    weights = []
    paths = []
    for wp in weight_paths:
        weights.append(wp[0])
        paths.append(wp[1:])
    return graph_id, paths, weights

    
def compute_results_from_files(p, t, start_k, end_k, instance_counts, num_combos,
                num_exp_types, results, col, row_offset, summary):
    # dicts to hold the data we want to count
    total_counts_unfiltered = defaultdict(int)
    total_counts = defaultdict(int)
    correct_counts = defaultdict(int)
    correct_k = defaultdict(int)
    incorrect_bc_non_opt = defaultdict(int)

    # walk over pred file p
    last_pos = p.tell()
    newline = p.readline()
    while newline != "":
        p.seek(last_pos)
        graph_id, pred_paths, pred_weights = get_next_predicted(p)
        # print("Predicted:")
        # print(pred_paths)
        # print(pred_weights)
        last_pos = p.tell()
        newline = p.readline()
        # print("this graph id is", graph_id)
        true_paths, true_weights = get_corresp_truth(t, graph_id)
        k = len(true_weights)

        # ignore instances not in k range
        if k >= start_k and k <= end_k:

            # if k is 4, we need all exp types to complete
            if k >= 4:
                all_completed = instance_counts[graph_id] == num_combos*num_exp_types
            elif k == 3:
                all_completed = instance_counts[graph_id] == num_combos*num_exp_types - 2
            elif k == 2:
                all_completed = instance_counts[graph_id] == num_combos*num_exp_types - 4

            total_counts_unfiltered[len(true_weights)] += 1
            if all_completed:
                total_counts[len(true_weights)] += 1
                if len(true_weights) == len(pred_weights):
                    correct_k[len(true_weights)] += 1
                if true_weights == pred_weights and true_paths == pred_paths:
                    correct_counts[len(true_weights)] += 1
                if true_weights != pred_weights or true_paths != pred_paths:
                    if len(true_paths) != len(pred_paths):
                        incorrect_bc_non_opt[len(true_weights)] += 1

    # print per-experiment information to console
    # print()
    # print("overall correct k:") 
    # print(sum(correct_k.values())/sum(total_counts_unfiltered.values()))
    # print("overall prop correct:") 
    # print(sum(correct_counts.values())/sum(total_counts.values()))
    # print("overall (filtered) intance count:") 
    # print(sum(total_counts.values()))
    # print("overall (unfiltered) intance count:") 
    # print(sum(total_counts_unfiltered.values()))
    # print("overall prop incor non opt:") 
    # print(sum(incorrect_bc_non_opt.values())/(sum(total_counts.values()) + sum(correct_counts.values())))
    # print()
    # print("key\tn\tprop.\tprop.\tprop.\ttot.\ttot.\t\tprop.")
    # print("\t\tcorrect\tcor. k\tcompl\tunfilt\tincor.\tincor non opt\tincor non opt")
    if summary:
        row = row_offset
        prop_correct = sum(correct_counts.values())/sum(total_counts.values())
        results[row][col + NUM_EXTRA_COLS - 1] = round(prop_correct, 3)
        results[row][0] = sum(total_counts_unfiltered.values())
        prop_finished = 0 if sum(total_counts_unfiltered.values()) == 0 else \
            sum(total_counts.values())/sum(total_counts_unfiltered.values())
        results[row][1] = f"{prop_finished*100:.2f}\%"
        results[row][2] = ""
    else:
        for key in sorted(total_counts.keys()):
            prop_correct = 0 if total_counts[key] == 0 else correct_counts[key]/total_counts[key]
            prop_correct_k = 0 if total_counts[key] == 0 else correct_k[key]/total_counts[key]
            prop_finished = 0 if total_counts_unfiltered[key] == 0 else total_counts[key]/total_counts_unfiltered[key]
            tot_incorrect_bc_non_opt = incorrect_bc_non_opt[key]
            tot_incorrect = total_counts[key] + correct_counts[key]
            prop_incor_non_opt = 0 if tot_incorrect == 0 else tot_incorrect_bc_non_opt/tot_incorrect
            print(f"{key}\t{total_counts[key]}\t" +
              f"{prop_correct:.3f}" +
              f"\t{prop_correct_k:.5f}" +
              f"\t{prop_finished:2f}",
              f"\t{total_counts_unfiltered[key]}",
              f"\t{tot_incorrect}",
              f"\t{tot_incorrect_bc_non_opt}",
              f"\t\t{prop_incor_non_opt:5f}")

            prop_correct = 0 if total_counts[key] == 0 else correct_counts[key]/total_counts[key]
            print(f"k={key}, prop cor = {prop_correct}")
            row = num_exp_types * key + row_offset - start_k * num_exp_types
            results[row][col + NUM_EXTRA_COLS] = round(prop_correct, 3)

        # add informational columns, but only in the heuristic rows
        if row_offset == 0:
            results[row][0] = key
            results[row][1] = total_counts_unfiltered[key]
            results[row][2] = f"{prop_finished*100:.2f}\%"
            results[row][3] = "H-br"
        else:
            results[row][0] = ""
            results[row][1] = ""
            results[row][2] = ""
            results[row][3] = "FPT"


if __name__ == "__main__":
    #### INPUTS ####

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', default="acyclic_sc_graph_instances")
    parser.add_argument('--min_k', default=2, type=int)
    parser.add_argument('--max_k', default=10, type=int)
    parser.add_argument('--fpt', default=False, action='store_true')
    parser.add_argument('--fd_heur', default=False, action='store_true')
    parser.add_argument('--fd_heur_no_br', default=False, action='store_true')
    parser.add_argument('--summary', default=False, action='store_true')
    args = parser.parse_args()

    data_dir = Path(args.input_dir)

    lengths = [3, 4]
    subpaths = [1, 2, 3, 4]
    combos = list(itertools.product(lengths, subpaths))
    combos = [(1, 0)] + combos  # for no subpath experiment

    start_k = args.min_k
    end_k = args.max_k

    exp_types = []
    if args.fd_heur:
        exp_types.append('fd_heur')
    if args.fpt:
        exp_types.append('fpt')
    if args.fd_heur_no_br:
        exp_types.append('fd_heur_no_br')

    # make array for storing results
    # if summary, we just need rows for exp types and we don't need a column
    # for k
    if args.summary:
        rows = len(exp_types)
        columns = len(combos) + NUM_EXTRA_COLS - 1
    # if not summary, we need more rows and cols. e.g., 
    # start_k=9 and end_k=10 and two exp_types, we have 4 rows
    # we have # different experiment combos + 4 columns (for k, n, pc,
    # exp_type)
    else:
        rows = (end_k - start_k + 1) * len(exp_types)
        columns = len(combos) + NUM_EXTRA_COLS 
    results = np.zeros([rows, columns]).tolist()
    # dict to store counts of completed instances
    instance_counts = defaultdict(int)
    true_paths = dict()
    true_weights = dict()
    pred_paths = dict()
    pred_weights = dict()
    pred_runtimes = dict()

    # combine predicted files and fill in instance counts dict
    print("Prepping data...")

    # get truth info
    exp_dir = f"len{combos[0][0]}dem1subpaths{combos[0][1]}"
    truth_file = data_dir / exp_dir / "truth/graphs.truth"
    print("  Processing groundtruth...")
    with open(truth_file, "r") as f:
        # walk over pred file f
        last_pos = f.tell()
        newline = f.readline()
        while newline != "":
            f.seek(last_pos)
            name, tp, tw = get_next_truth(f)
            true_paths[name] = tp
            true_weights[name] = tw
            last_pos = f.tell()
            newline = f.readline()

    # get pred and runtime info
    for length, sps in combos:
        for exp_type in exp_types:
            print(f"  Processing {length}, {sps}, {exp_type}")
            pred_paths[(length, sps, exp_type)] = dict()
            pred_weights[(length, sps, exp_type)] = dict()
            pred_runtimes[(length, sps, exp_type)] = dict()
            exp_dir = f"len{length}dem1subpaths{sps}"
            pred_dir = data_dir / exp_dir / f"predicted_{exp_type}"
            filenames = [str(f) for f in list(filter(Path.is_file, pred_dir.glob('**/pred*')))]
            filenames.sort(key=get_pred_filenum)
            # only do one file for now
            for filename in filenames:
                runtime_filename = filename.replace("predicted", "runtimes").replace("pred", "runtimes")
                with open(runtime_filename, "r") as f:
                    for line in f.readlines():
                        name = line.split(".")[0]
                        runtime = float(line.split(" ")[1])
                        pred_runtimes[(length, sps, exp_type)][name] = runtime
                with open(filename, "r") as f:
                    # walk over pred file f
                    last_pos = f.tell()
                    newline = f.readline()
                    while newline != "":
                        f.seek(last_pos)
                        name, pp, pw = get_next_predicted(f)
                        pred_paths[(length, sps, exp_type)][name] = pp
                        pred_weights[(length, sps, exp_type)][name] = pw
                        last_pos = f.tell()
                        newline = f.readline()

    # print(pred_paths)
    # print(pred_weights)
    # print(true_paths)
    # print(true_weights)
    # print(pred_runtimes)

    for exp_type in exp_types:
        min_ = 10000
        total = 0
        count = 0
        max_ = 0
        for length, sps in combos:
            for name in pred_runtimes[(length, sps, exp_type)].keys():
                if len(true_paths[name]) >= start_k and\
                     len(true_paths[name]) <= end_k:
                    min_ = min(min_, pred_runtimes[(length, sps, exp_type)][name])
                    max_ = max(max_, pred_runtimes[(length, sps, exp_type)][name])
                    count += 1
                    total += pred_runtimes[(length, sps, exp_type)][name]
        print(exp_type)
        print(f"min runtime is {round(min_, 3)}")
        print(f"max runtime is {round(max_, 3)}")
        print(f"avg runtime is {round(total/count, 3)}")

    # get runtime information

    # make table
    for col, (length, sps) in enumerate(combos):
        for row_offset, exp_type in enumerate(exp_types):
        
            print(f"Computing {exp_type}, {length}, {sps}...")
            # all k get done in here
            with open(pred_file, "r") as p, open(truth_file, "r") as t:
                compute_results_from_dicts(
                    # paramteres
                    start_k, end_k,
                    results, col, row_offset, args.summary,
                    # data dicts
                    instance_counts,
                    pred_paths,
                    pred_weights,
                    true_paths,
                    true_weights)
            print(results)

    # make latex table from file
    print_as_latex_table(results, len(exp_types))
