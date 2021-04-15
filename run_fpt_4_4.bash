#!/bin/bash  

rm -rf run_fpt_err/
rm -rf run_fpt_out/
rm -rf run_fpt_slurms/
mkdir run_fpt_err
mkdir run_fpt_out
mkdir run_fpt_slurms
    
for len in 4; do
    echo $len
    for sps in 4; do
        rm -rf "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fpt/"
        mkdir "acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/predicted_fpt/"
        echo $sps
        path="acyclic_sc_graph_instances/len${len}dem1subpaths${sps}/graphs/"
        echo $path
        numfiles=$(ls -l $path | wc -l)
        numfiles=$(($numfiles - 2))
        # numfiles=1

        for p in $(seq 0 $numfiles); do
            filename=$path'sc'$p'.graph'
            echo $filename
        
echo '#!/bin/bash
 
#SBATCH --job-name    '$len'_'$sps'_'$p'run_fpt_data        # job name
#SBATCH --output      run_fpt_out/'$len'_'$sps'_'$p'.out # standard output file (%j = jobid)
#SBATCH --error       run_fpt_err/'$len'_'$sps'_'$p'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         20000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        2:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE
 
python ../coaster/coaster.py '$filename' --timeout 30' > run_fpt_slurms/${len}_${sps}_${p}.slurm
sbatch run_fpt_slurms/${len}_${sps}_${p}.slurm
done
done
done
