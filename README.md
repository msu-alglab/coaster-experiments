This repository holds scripts to create input data for and analyze the results
of Coaster (https://github.com/msu-alglab/coaster), software for decomposing
cyclic flows.

It will also contain scripts for running experiments on Hyalite, MSU's research
computing cluster.

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
* a directory for outputting the graph instance files
* a filename for writing the ground truth paths
* *R*, the length of subpaths to generate (length of subpaths in the contracted
	graph)
* a boolean indicating whether subpaths should have full weight (if `False`,
	subpaths have weight 1)
* *l*, the number of subpaths to generate

To generate subpaths, we fix an arbitrary ordering of the groundtruth paths and
take the first *l* of these. For each, we create a subpath as the first *R*
edges (*R* + 1 nodes) in the path.

#### Example

To create cyclic instances from basic Toboggan inputs in the `basic_instances`
directory and output cyclic instances in the `cyclic_instances` directory,
we can run

```
python create_cyclic_instances.py basic_instances/ cyclic_instances/
```

Then, we can add subpaths to the instances in `cyclic_instances`. TODO
