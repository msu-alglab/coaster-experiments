This repository holds scripts to create input data for and analyze the results
of [Coaster](https://github.com/msu-alglab/coaster), software for decomposing
flows.

It also contains scripts for running experiments on
[Hyalite](https://www.montana.edu/uit/rci/hyalite/), MSU's research computing
cluster.

Scripts can be run using Python 3.

In this readme, we first describe how to run experiments, and then describe
each of the scripts used in detail.


### To run experiments for WABI 2021

#### Environment

On Hyalite, I first do the following:

```
module load Python/3.7.2-GCCcore-8.2.0
module load OpenSSL/1.1.1b-GCCcore-8.2.0

export OPENBLAS_NUM_THREADS=2
export GOTO_NUM_THREADS=2
export OMP_NUM_THREADS=2
```
The `export` statements are for Numpy.

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

### To run experiments for journal updates for TCBB:

There are two experiments added here.

1. Investigation of runtime vs. memory use.

 To look at this, we run graphs one at a time. First, we look at 1,999
instances with 4 length 4 subpaths (from the file
`acyclic_sc_graph_instances/len4dem1subpaths4/sc0.graph` and let them run for
an hour by running
```
bash run_one_job_per_instance.bash
```
Here we see that even graphs that take 25 minutes only have 80MB Max RSS,
whereas simply loading the needed Python packages (and doing nothing else)
 uses 57MB Max RSS.

We can also look at large graphs and let them run for three hours. Specifically, create graphs using

```
python create_sc_instances.py basic_instances/ acyclic_sc_graph_instances/ 4 False 4 100000 100 8
```
but save them in `big_instances/len4dem1subpaths4/graphs/sc0.graph`. Then use
```
bash run_big_instances.bash
```
to run each with a 3 hour time limit.

*below is what we want to do*

To investigate memory use, we look only at graphs with k=9 and k=10. To create
this data set, we run

```  
bash create_memtest_data.bash
```  
Then, to run each of the graphs as a separate job on Hyalite with a timeout of
1 hour, we run
```  
bash run_memtest.bash
```  


2. todo

### To create data for RECOMB 2021 (integer linear program)

*Pre-computed data can be found at https://drive.google.com/drive/folders/15l1lhTRVNG_2tFUZtmwSZJvv2YG_HY-k?usp=sharing*

To create subpath constraint instances from the human dataset from Catfish, put
the `.graph` and `.truth` files in the directory `basic_instances` and run
```
python create_sc_instances.py basic_instances/ acyclic_sc_graph_instances/ 3 False 4 1000000 1000
```
to create instances with 4 subpath constraints, 3 edges, with up to 1,000,000 instances per file, a max k value of 1000
(i.e., allow all instances to go in the same file, and do not limit by k).

To create subpath constraint instances from our data simulated from human gene
annotations and a stringtie run, put the output of those scripts in the
directory and run. For example, if we put the human annotation data as `human`
and stringtie as `SRR307903_assembly`, we can run

```
python create_sc_instances.py human/ human_annotation_sc_graph_instances/ 3 False 4 1000000 1000
python create_sc_instances.py SRR307903_assembly/ SRR307903_assembly_sc_graph_instances/ 3 False 4 1000000 1000
```

These files can be found in the Google Drive linked above.

### Details about Python and Bash scripts

#### Creating data

Coaster inputs are DAGs, possibly  with subpath constraints.
`create_sc_instances.py` adds subpaths to original Toboggan inputs.
`create_sc_instances.py` takes the following parameters:
* an input directory containing a graph instance file and a ground truth file i.e.,
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
`output_dir/len[R]dem[full/1]subpaths[l]/truth/graphs.truth`.

As many graph files as necessay will be created as
`output_dir/len[r]dem[full/1]subpaths[l]/graphs/sc[num].graph`.


##### Example

```
python create_sc_instances.py basic_instances/ acyclic_sc_graph_instances/ 2 False 2 100000 100
```
creates a subpath constraint instances in the
`acyclic_sc_graph_instances/len2dem1subpath2/` directory, all in the
`sc0.graph` file, with max k of 100.

#### Scripts for Hyalite cluster

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

##### run_one_job_per_instance.bash

In order to check the memory use for each instance, we run `coaster.py` only on
one instance at a time. This script creates a `slurm` file (and runs it) for
each of the 1,999 instances in `acyclic_sc_graph_instances/len4dem1subpaths4/graphs/sc0.graph`.
It uses `/usr/bin/time` to write the max RSS to std error.

##### run_big_instances.bash

Similar to the above, this runs 30 large (k >= 8) instances in `big_instances/len4dem1subpaths4/graphs/sc0.graph`
with a max time of 3 hours.

##### full_experiment_postprocess.py

For each of the experiment types given (using `--fpt` flag and/or `--fd_heur`
flag), combines all of the individual prediction files into one single
prediction file in same order as truth file. Will also generate data for
restricting output to only instances that ran to completion for all
experiments. (For k=2 through k=8 only).

##### compute_results.py

For each experiment type given (using `--fpt` and `--fd_heur`), computes
accuracies from the combined pred files and instance counts.
