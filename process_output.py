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
    pred_dir = Path(args.output_dir)
    pred_file = open(pred_dir, "r")
    truth_file = open(truth_dir, "r")

    total_counts = defaultdict(int)
    correct_counts = defaultdict(int)
    correct_k = defaultdict(int)

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
        # print("True:")
        # print(true_paths)
        # print(true_weights)
        total_counts[len(true_weights)] += 1
        if len(true_weights) == len(pred_weights):
            correct_k[len(true_weights)] += 1
        if true_weights == pred_weights and true_paths == pred_paths:
            # print("Correct")
            correct_counts[len(true_weights)] += 1
    print()
    print("key\tn\tprop.\tprop.")
    print("\t\tcorrect\tcorrect k")
    f = open("all_outputs.txt", "a")
    if 2 not in total_counts.keys():
        f.write("0,")
    if 3 not in total_counts.keys():
        f.write("0,")
    for key in sorted(total_counts.keys()):
        print(f"{key}\t{total_counts[key]}\t" +
              f"{correct_counts[key]/total_counts[key]:.2f}" +
              f"\t{correct_k[key]/total_counts[key]:.2f}")
    for key in list(sorted(total_counts.keys()))[:-1]:
        f.write(f"{correct_counts[key]/total_counts[key]:.3f},")
    last_key = list(sorted(total_counts.keys()))[-1]
    f.write(f"{correct_counts[last_key]/total_counts[last_key]:.3f}")
    f.write("\n")
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("truth_dir",
                        help="A directory containing the ground truth file")
    parser.add_argument("output_dir",
                        help="A directory containing the predicted paths")
    args = parser.parse_args()
    main(args)
