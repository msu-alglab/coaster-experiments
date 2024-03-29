#!/bin/bash  

rm -rf run_memtest_heuristic_err/
rm -rf run_memtest_heuristic_out/
rm -rf run_memtest_heuristic_slurms/
mkdir run_memtest_heuristic_err
mkdir run_memtest_heuristic_out
mkdir run_memtest_heuristic_slurms
    
for len in 3 4; do
    echo $len
    for sps in 1 2 3 4; do
        rm -rf "memtest_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fd_heur/"
        mkdir "memtest_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fd_heur/"
        path="memtest_sc_graph_instances/len${len}dem1subpaths${sps}/graphs/"
        filename="${path}sc999999999.graph"
        # assume there are fewer then 3000 files
        cat ${path}sc{0..3000}.graph > $filename
        
echo '#!/bin/bash
 
#SBATCH --job-name    '$len'_'$sps'_'$p'run_memtest_heuristic_data        # job name
#SBATCH --output      run_memtest_heuristic_out/'$len'_'$sps'_'$p'.out # standard output file (%j = jobid)
#SBATCH --error       run_memtest_heuristic_err/'$len'_'$sps'_'$p'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         2000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        2:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE
 
/usr/bin/time -f "%M" python ../coaster/coaster.py '$filename' --timeout 3600 --fd_heuristic
rm '$filename'' > run_memtest_heuristic_slurms/${len}_${sps}_${p}.slurm
sbatch run_memtest_heuristic_slurms/${len}_${sps}_${p}.slurm
done
done

for len in 1; do
    echo $len
    for sps in 0; do
        rm -rf "memtest_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fd_heur/"
        mkdir "memtest_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fd_heur/"
        path="memtest_sc_graph_instances/len${len}dem1subpaths${sps}/graphs/"
        filename="${path}sc999999999.graph"
        # assume there are fewer then 3000 files
        cat ${path}sc{0..3000}.graph > $filename
        
echo '#!/bin/bash

#SBATCH --job-name    '$len'_'$sps'_'$p'run_memtest_heuristic_data        # job name
#SBATCH --output      run_memtest_heuristic_out/'$len'_'$sps'_'$p'.out # standard output file (%j = jobid)
#SBATCH --error       run_memtest_heuristic_err/'$len'_'$sps'_'$p'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         2000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        2:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE

/usr/bin/time -f "%M" python ../coaster/coaster.py '$filename' --timeout 3600 --fd_heuristic
rm '$filename'' > run_memtest_heuristic_slurms/${len}_${sps}_${p}.slurm
sbatch run_memtest_heuristic_slurms/${len}_${sps}_${p}.slurm
done
done
