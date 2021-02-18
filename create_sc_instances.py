import argparse
import os
import shutil
from toboggan.parser import read_instances
import time


def write_sc(sc, of, graph, mapping, dem_full, paths, weights):
    real_path = []
    for arc in sc:
        real_path.extend(mapping[arc])
    node_seq = [graph.arc_info[real_path[0]]['start']]
    for arc in real_path:
        node_seq.append(graph.arc_info[arc]['destin'])

    demand = 0
    if dem_full:
        for w, path in zip(weights, paths):
            if str(sc)[1:-1] in str(path)[1:-1]:
                demand += w
    else:
        demand = 1
    of.write("{} {}\n".format(" ".join([str(x) for x in node_seq]),
                              float(demand)))

def create_and_write_scs(reduced, mapping, graph, solutions, of, ell, # noqa
                         length, dem_full, counter):
    reduced_sols = []
    for solution in solutions:
        path = reduced.produce_contracted_path(
            solution[1], mapping, graph)
        reduced_sols.append((solution[0], path))
    weights = [x[0] for x in reduced_sols]
    paths = [x[1] for x in reduced_sols]

    if counter % 5000 == 0:
        print("# processed", counter, "graphs")
    counter += 1
    graph.write(of)
    of.write("subpaths\n")
    for w, p in reduced_sols[:ell]:
        sc = p[:length]
        write_sc(sc, of, graph, mapping, dem_full, paths, weights)
    return counter


def create_truth_file(truth_out, directory, truth_files):
    f = open(truth_out, "w")
    for file in truth_files:
        print("looking at truth file", file)
        file_name = file.split("/")[-1]
        tf = open(directory + file, "r")
        next_line = tf.readline()
        while next_line != "":
            if next_line[0] == "#":
                number = next_line.split("number = ")[1].split(" ")[0]
                start = next_line.split("name = ")[0] + "name = "
                next_line = start + number + "-" + file_name + "\n"
            f.write(next_line)
            next_line = tf.readline()
    f.close()


def main(args):

    directory = args.dir
    dem_full = args.dem == "True"
    if dem_full:
        dem = "full"
    else:
        dem = "1"
    print("graph and truth files are in", directory)
    files = os.listdir(directory)
    graph_files = sorted([x for x in files if x.split(".")[1] == "graph"])
    truth_files = sorted([x for x in files if x.split(".")[1] == "truth"])
    print(graph_files)
    print(truth_files)
    truth_out = args.truth_out_file_prefix + ".len{}dem{}subpaths{}".format(
        args.len, dem, args.ell) + ".truth"
    create_truth_file(truth_out, directory, truth_files)
    start_time = time.time()
    outputprefix = "{}/len{}dem{}".format(args.graph_out_dir, args.len, dem)
    print("doing {}, {} experiment".format(args.len, dem))
    output = outputprefix + "subpaths" + str(args.ell) + "/"
    print("# writing files in", output)
    print("# Time:", round(time.time() - start_time), "seconds")
    if os.path.exists(output):
        shutil.rmtree(output)
    if not os.path.exists(args.graph_out_dir):
        os.mkdir(args.graph_out_dir)
    os.mkdir(output)

    counter = 1

    of = open(output + "sc" + str(counter//args.g_p_file)
              + ".graph", "w")
    for graph_file, truth_file in zip(graph_files, truth_files):
        print("# processing graph file", graph_file)
        graph_file = directory + graph_file
        truth_file = directory + truth_file
        for graphdata, solutions, _ in read_instances(graph_file,
                                                      truth_file):
            graph, graphname, graphnumber = graphdata
            reduced, mapping = graph.contracted()
            if len(solutions) >= args.ell and len(solutions) > 1:
                counter = create_and_write_scs(
                    reduced, mapping, graph, solutions, of, args.ell,
                    args.len, dem_full, counter)
                if counter % args.g_p_file == 0:
                    of.close()
                    of = open(
                        output + "sc" +
                        str(counter//args.g_p_file) +
                        ".graph", "w")
    of.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("num_sc", help="number of subpaths to create",
    #                    type=str)
    parser.add_argument('dir',
                        help='A directory containing the input .graph and' +
                        '.truth files')
    parser.add_argument('graph_out_dir',
                        help='A directory for the output graph files')
    parser.add_argument('truth_out_file_prefix',
                        help='A prefix for the output truth file')
    parser.add_argument('len', help="length of subpaths", type=int)
    parser.add_argument("dem", help="demand of subpaths")
    parser.add_argument("ell", help="ell of subpaths", type=int)
    parser.add_argument("g_p_file", help="graphs per file", type=int)
    args = parser.parse_args()
    main(args)
