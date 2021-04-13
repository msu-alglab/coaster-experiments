#!/bin/bash  

rm -rf run_heuristic_err/
rm -rf run_heuristic_out/
rm -rf run_heuristic_slurms/
mkdir run_heuristic_err
mkdir run_heuristic_out
mkdir run_heuristic_slurms
    
for len in 3 4; do
    echo $len
    for sps in 1 2 3 4; do
        echo $sps
        
echo '#!/bin/bash

#SBATCH --job-name    '$len'_'$sps'run_heuristic_data        # job name
#SBATCH --output      run_heuristic_out/'$len'_'$sps'.out # standard output file (%j = jobid)
#SBATCH --error       run_heuristic_err/'$len'_'$sps'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         5000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        12:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE

python ../coaster/coaster.py
acyclic_sc_graph_instances/len'$len'dem1subpaths'$sps'/graphs/sc0.graph --fd_heuristic' > run_heuristic_slurms/$len_$sps.slurm
sbatch run_heuristic_slurms/$len_$sps.slurm
done
done

for len in 1; do
    echo $len
    for sps in 0; do
        echo $sps
        
echo '#!/bin/bash

#SBATCH --job-name    '$len'_'$sps'run_heuristic_data        # job name
#SBATCH --output      run_heuristic_out/'$len'_'$sps'.out # standard output file (%j = jobid)
#SBATCH --error       run_heuristic_err/'$len'_'$sps'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         5000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        12:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE

python ../coaster/coaster.py
acyclic_sc_graph_instances/len'$len'dem1subpaths'$sps'/graphs/sc0.graph --fd_heuristic' > run_heuristic_slurms/$len_$sps.slurm
sbatch run_heuristic_slurms/$len_$sps.slurm
done
done
