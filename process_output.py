import argparse
from collections import defaultdict
from pathlib import Path


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
            # print("this graph id is", this_graph_id)
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


def main(args):
    truth_dir = Path(args.truth_dir)
    # get instance count for filtering instances that didn't complete for all
    # experiments
    print("truth_dir is", truth_dir)
    length = int(str(truth_dir).split("acyclic_sc_graph_instances/len")[1].split("dem")[0])
    sps = int(str(truth_dir).split("/truth")[0].split("subpaths")[1])
    print("length=", length, "sps=", sps)
    instance_counts = defaultdict(int)
    with open("instance_counts.txt") as f:
        for line in f:
            key = line.split()[0].strip()
            value = int(line.split()[1].strip())
            instance_counts[key] = value
    pred_dir = Path(args.output_dir)
    pred_file = open(pred_dir, "r")
    truth_file = open(truth_dir, "r")

    total_counts_unfiltered = defaultdict(int)
    total_counts = defaultdict(int)
    correct_counts = defaultdict(int)
    correct_k = defaultdict(int)
    incorrect_bc_non_opt = defaultdict(int)
    # we want entries for 2 through 10
    for k in range(2, 11):
        total_counts[k] = 0
        correct_counts[k] = 0
        correct_k[k] = 0

    last_pos = pred_file.tell()
    newline = pred_file.readline()
    while newline != "":
        pred_file.seek(last_pos)
        graph_id, pred_paths, pred_weights = get_next_predicted(pred_file)
        # print("Predicted:")
        # print(pred_paths)
        # print(pred_weights)
        last_pos = pred_file.tell()
        newline = pred_file.readline()
        true_paths, true_weights = get_corresp_truth(truth_file, graph_id)
        k = len(true_weights)
        # print("True:")
        # print(true_paths)
        # print(true_weights)
        if k == 2:
            count = 10 
        elif k == 3:
            count = 14 
        else:
            count = 18
        total_counts_unfiltered[len(true_weights)] += 1
        if instance_counts[graph_id] == count or k >= 9:
            total_counts[len(true_weights)] += 1
            if len(true_weights) == len(pred_weights):
                correct_k[len(true_weights)] += 1
            if true_weights == pred_weights and true_paths == pred_paths:
                # print("Correct")
                correct_counts[len(true_weights)] += 1
            if true_weights != pred_weights or true_paths != pred_paths:
                if len(true_paths) != len(pred_paths):
                    incorrect_bc_non_opt[len(true_weights)] += 1
    print()
    print("overall correct k:") 
    print(sum(correct_k.values())/sum(total_counts_unfiltered.values()))
    print("overall prop correct:") 
    print(sum(correct_counts.values())/sum(total_counts.values()))
    print("overall (filtered) intance count:") 
    print(sum(total_counts.values()))
    print("overall prop incor non opt:") 
    print(sum(incorrect_bc_non_opt.values())/(sum(total_counts.values()) + sum(correct_counts.values())))
    print()
    print("key\tn\tprop.\tprop.\tprop.\ttot.\ttot.\t\tprop.")
    print("\t\tcorrect\tcor. k\tcompl\tunfilt\tincor.\tincor non opt\tincor non opt")
    f = open("all_outputs.txt", "a")
    if 2 not in total_counts.keys():
        f.write("0,")
    if 3 not in total_counts.keys():
        f.write("0,")
    for key in sorted(total_counts.keys()):
        prop_correct = 0 if total_counts[key] == 0 else\
correct_counts[key]/total_counts[key]
        prop_correct_k = 0 if total_counts[key] == 0 else\
correct_k[key]/total_counts[key]
        prop_finished = 0 if total_counts_unfiltered[key] == 0 else\
total_counts[key]/total_counts_unfiltered[key]
        tot_incorrect_bc_non_opt = incorrect_bc_non_opt[key]
        tot_incorrect = total_counts[key] + correct_counts[key]
        prop_incor_non_opt = 0 if tot_incorrect == 0 else \
tot_incorrect_bc_non_opt/tot_incorrect
        print(f"{key}\t{total_counts[key]}\t" +
              f"{prop_correct:.3f}" +
              f"\t{prop_correct_k:.5f}" +
              f"\t{prop_finished:2f}",
              f"\t{total_counts_unfiltered[key]}",
              f"\t{tot_incorrect}",
              f"\t{tot_incorrect_bc_non_opt}",
              f"\t\t{prop_incor_non_opt:5f}")
    for key in list(sorted(total_counts.keys()))[:-1]:
        prop_correct = 0 if total_counts[key] == 0 else\
                correct_counts[key]/total_counts[key]
        f.write(f"{prop_correct:.3f},")
    last_key = list(sorted(total_counts.keys()))[-1]
    prop_correct = 0 if total_counts[last_key] == 0 else\
correct_counts[last_key]/total_counts[last_key]
    f.write(f"{prop_correct:.3f}\n")
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("truth_dir",
                        help="A directory containing the ground truth file")
    parser.add_argument("output_dir",
                        help="A directory containing the predicted paths")
    args = parser.parse_args()
    main(args)
