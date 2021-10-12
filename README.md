This repository holds scripts to create input data for and analyze the results
of Coaster (https://github.com/msu-alglab/coaster), software for decomposing
flows.

It also contains scripts for running experiments on
(Hyalite)[https://www.montana.edu/uit/rci/hyalite/], MSU's research computing
cluster.

Scripts can be run using Python 3.

### Creating Data

`create_cyclic_instances.py` creates cyclic flow instances (without subpath
constraints) from original toboggan instances. For each ground truth path in
the toboggan path, a second path is created by randomly permuting the exons of
the path. Only instances with at least two ground truth paths are generated.

`create_cyclic_instances.py` takes the following parameters:
* an input directory containing graph instance file(s) and ground truth file(s)
* an output directory in which to write the output graph instance file(s) and
	ground truth file(s)
* optionally, a seed for generating the same random outputs each time

Coaster inputs are (possibly) cyclic graphs with subpath constraints.
`create_sc_instances.py` adds
subpaths to the cyclic flow instances output by `create_cyclic_instances.py`, or to
original Toboggan inputs.
`create_sc_instances.py` takes the following parameters:
* an input directory containing a graph instance file and a ground truth file
	(can by cyclic, e.g., output by `create_cyclic_instances.py`, or acyclic, e.g.,
	original Toboggan inputs)
* a directory for outputting graph and truth files
* *R*, the length of subpaths to generate (length of subpaths in the contracted
	graph)
* a boolean indicating whether subpaths should have full weight (if `False`,
	subpaths have weight 1) *TODO: make this an optional flag for full
	weight*
* *l*, the number of subpaths to generate
* *g_p_file*, the number of graphs to be written to each separate `.graph` file
    (in order to run many graph instances in parallel on Hyalite). Input a
    large number to put all graphs in one file. *TODO: make
    this optional*
* *max_k*, the largest k value to keep for instances (determined by looking at
  ground truth data)

To generate subpaths, we fix an arbitrary ordering of the groundtruth paths and
take the first *l* of these. For each, we create a subpath as the first *R*
edges (*R* + 1 nodes) in the path.

A single truth file will be created and it will be placed in
`output_dir/len*R*dem*full/1*subpaths*l*/truth/graphs.truth`.

As many graph files as necessay will be created as
`output_dir/len*r*dem*full/1*subpaths*l*/graphs/sc*num*.truth`.


#### Examples

##### Cyclic subpath constraint instances

To create cyclic instances from basic Toboggan inputs in the `basic_instances`
directory and output cyclic instances in the `cyclic_instances` directory,
we can run

```
python create_cyclic_instances.py basic_instances/ cyclic_instances/
```

Then, we can add subpaths to the instances in `cyclic_instances`.

```
python create_sc_instances.py cyclic_instances/ cyclic_sc_graph_instances/ 2 True 2 100000 100
```
In this example, subpath constraints are length 2, are full weight, and there
are 2 of them. 100,000 graphs should be put in each file (since there are only
20,000 graphs in the input, this will put all graphs into one file).

##### Acyclic subpath constraint instances

If we don't want to add cycles to the basic Toboggan instances, we can run, for
example,

```
python create_sc_instances.py basic_instances/ acyclic_sc_graph_instances/ 2 False 2 100000 100
```
which creates a subpath constraint instances in the
`acyclic_sc_graph_instances/len2dem1subpath2/` directory, all in the
`sc0.graph` file, with max k of 100.

### Scripts for Hyalite cluster

We can run large data sets on the Hyalite cluster using the following bash
scripts. For each set of experimental conditions, they create a slurm script
and then run it using `sbatch`.

##### create_acyclic_data.bash

Runs `create_sc_instances.py` on whatever is in `basic_instances/` directory,
as in example above, for the set of subpath lengths and numbers of subpaths
hard coded into the bash script.

##### run_heuristic.bash

Runs `coaster.py` on the specified files in `acyclic_sc_graph_instances/` directory.
The files are specified as a set of experimental conditions that are hard-coded
into the bash script. Uses the `--fd_heuristic` flag when running Coaster.

##### run_fpt.bash

Runs `coaster.py` on the specified files in `acyclic_sc_graph_instances/` directory.
The files are specified as a set of experimental conditions that are hard-coded
into the bash script. Uses the `--timeout` flag to set a max time, which is
hard coded in the file

##### full_experiment_postprocess.py

For each of the experiment types given (using `--fpt` flag and/or `--fd_heur`
flag), combines all of the individual prediction files into one single
prediction file in same order as truth file. Will also generate data for
restricting output to only instances that ran to completion for all
experiments. (For k=2 through k=8 only).

##### compute_results.py

For each experiment type given (using `--fpt` and `--fd_heur`), computes
accuracies from the combined pred files and instance counts.

#### To run experiments for WABI 2021
The human data set from (Catfish
test)[https://github.com/Kingsford-Group/catfishtest] should be in the
`basic_instances` directory.
1. Use `create_acyclic_data.bash` to create data. (Takes...1 hour? Maybe less.)
2. Use `run_heuristic.bash` to run the heuristic on the data. (Takes 3 hours.
   On hyalite, it seems that there is an issue with preemption when the memory
allocated to jobs is small. So maybe worth allocating more memory.)
3. Use `run_fpt.bash` to run the heuristic on the data. (Takes 5 hours.
Again maybe better to allocate more data.)
4. Use `full_experiment_postprocess.py --fpt --fd_heur` to combine all
   individual pred files into one, and also create a file with every graph name
that completed for all runs (but include all for 9 and 10), so that we can
filter results by instances that completed for all runs.
5. Use `compute_results.py --fpt --fd_heur` to compute accuracies for all
   instances that completed for all runs (and all for k=9 and k=10).
6. Use `compute_runtimes_memuse.py --fpt --fd_heur` to compute runtimes and
   peak memory use info for |R|=4, ell=4 instances.
