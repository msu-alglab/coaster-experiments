#!/bin/bash  

rm -rf run_heuristic_no_br_err/
rm -rf run_heuristic_no_br_out/
rm -rf run_heuristic_no_br_slurms/
mkdir run_heuristic_no_br_err
mkdir run_heuristic_no_br_out
mkdir run_heuristic_no_br_slurms
   
for len in 3 4; do
    echo $len
    for sps in 1 2 3 4; do
        rm -rf "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fd_heur_no_br/"
        mkdir "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fd_heur_no_br/"
        rm -rf "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/runtimes_fd_heur_no_br/"
        mkdir "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/runtimes_fd_heur_no_br/"
        echo $sps
        path="acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/graphs/"
        echo $path
        numfiles=$(ls -l $path | wc -l)
        numfiles=$(($numfiles - 2))

        for p in $(seq 0 $numfiles); do
            filename=$path'sc'$p'.graph'
            echo $filename
        
echo '#!/bin/bash
 
#SBATCH --job-name    '$len'_'$sps'_'$p'run_heuristic_no_br_data        # job name
#SBATCH --output      run_heuristic_no_br_out/'$len'_'$sps'_'$p'.out # standard output file (%j = jobid)
#SBATCH --error       run_heuristic_no_br_err/'$len'_'$sps'_'$p'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         1000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        :30:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE
 
python ../coaster/coaster.py '$filename' --fd_heuristic_no_br' > run_heuristic_no_br_slurms/${len}_${sps}_${p}.slurm
sbatch run_heuristic_no_br_slurms/${len}_${sps}_${p}.slurm
done
done
done

for len in 1; do
    echo $len
    for sps in 0; do
        echo $sps
        rm -rf "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fd_heur_no_br/"
        mkdir "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fd_heur_no_br/"
        rm -rf "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/runtimes_fd_heur_no_br/"
        mkdir "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/runtimes_fd_heur_no_br/"
        path="acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/graphs/"
        echo $path
        numfiles=$(ls -l $path | wc -l)
        numfiles=$(($numfiles - 2))

        for p in $(seq 0 $numfiles); do
            filename=$path'sc'$p'.graph'
            echo $filename
        
echo '#!/bin/bash

#SBATCH --job-name    '$len'_'$sps'_'$p'run_heuristic_no_br_data        # job name
#SBATCH --output      run_heuristic_no_br_out/'$len'_'$sps'_'$p'.out # standard output file (%j = jobid)
#SBATCH --error       run_heuristic_no_br_err/'$len'_'$sps'_'$p'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         1000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        :30:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE

python ../coaster/coaster.py '$filename' --fd_heuristic_no_br' > run_heuristic_no_br_slurms/${len}_${sps}_${p}.slurm
sbatch run_heuristic_no_br_slurms/${len}_${sps}_${p}.slurm
done
done
done
