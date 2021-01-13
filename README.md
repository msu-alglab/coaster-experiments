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
