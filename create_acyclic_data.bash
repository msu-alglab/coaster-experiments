#!/bin/bash  

rm -rf create_acyclic_err/
rm -rf create_acyclic_out/
rm -rf create_acyclic_slurms/
mkdir create_acyclic_err
mkdir create_acyclic_out
mkdir create_acyclic_slurms
    
for len in 3 4; do
    echo $len
    for sps in 1 2 3 4; do
        echo $sps
        
echo '#!/bin/bash

#SBATCH --job-name    '$len'_'$sps'create_acyclic_data        # job name
#SBATCH --output      create_acyclic_out/'$len'_'$sps'.out # standard output file (%j = jobid)
#SBATCH --error       create_acyclic_err/'$len'_'$sps'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         1000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        2:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE

python create_sc_instances.py basic_instances/ acyclic_sc_graph_instances/ '$len' False '$sps' 2000 10' > create_acyclic_slurms/$len_$sps.slurm
sbatch create_acyclic_slurms/$len_$sps.slurm
done
done

for len in 1; do
    echo $len
    for sps in 0; do
        echo $sps
        
echo '#!/bin/bash

#SBATCH --job-name    '$len'_'$sps'create_acyclic_data        # job name
#SBATCH --output      create_acyclic_out/'$len'_'$sps'.out # standard output file (%j = jobid)
#SBATCH --error       create_acyclic_err/'$len'_'$sps'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         1000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        2:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE

python create_sc_instances.py basic_instances/ acyclic_sc_graph_instances/ '$len' False '$sps' 2000 10' > create_acyclic_slurms/$len_$sps.slurm
sbatch create_acyclic_slurms/$len_$sps.slurm
done
done
