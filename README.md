`create_cf_instances.py` creates cyclic flow instances (without subpath
constraints) from original toboggan instances. For each ground truth path in
the toboggan path, a second path is created by randomly permuting the exons of
the path. Only instances with at least two ground truth paths are generated.

`create_cf_instances.py` takes the following parameters:
* an input directory containing a graph instance file and a ground truth file
	(e.g., `1.graph` and `1.truth`)
* an output directory in which to write the output graph instance file(s) and
	ground truth file(s)
* optionally, a seed for generating the same random outputs

Coaster inputs are (possibly) cyclic graphs with subpath constraints.
`create_sc_instances.py` adds
subpaths to the cyclic flow instances output by `create_cf_instances.py`.
`create_sc_instances.py` takes the following parameters:
* an input directory containing a graph instance file and a ground truth file
	(can by cyclic or acyclic)
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
