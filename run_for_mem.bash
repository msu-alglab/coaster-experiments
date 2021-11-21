for INDEX in {1..31}
do
    /usr/bin/time -v python ~/coaster/coaster.py acyclic_sc_graph_instances/len4dem1subpaths4/graphs/sc0.graph --indices $INDEX --timeout 30 > std_out_files/out$INDEX.txt 2> std_error_files/error$INDEX.txt
done

