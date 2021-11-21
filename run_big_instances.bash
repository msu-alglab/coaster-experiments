#!/bin/bash  

rm -rf run_big_instances_err/
rm -rf run_big_instances_out/
rm -rf run_big_instances_slurms/
mkdir run_big_instances_err
mkdir run_big_instances_out
mkdir run_big_instances_slurms
    
for instance in $(seq 30); do

echo "${instance}"
        
echo '#!/bin/bash
 
#SBATCH --job-name    '$instance'_big        # job name
#SBATCH --output      run_big_instances_out/'$instance'.out # standard output file (%j = jobid)
#SBATCH --error       run_big_instances_err/'$instance'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         1000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        4:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE
 
/usr/bin/time -f "%M" python ../coaster/coaster.py big_instances/len4dem1subpaths4/graphs/sc0.graph --indices '$instance' --timeout 10800' > run_big_instances_slurms/"${instance}".slurm
sbatch run_big_instances_slurms/"${instance}".slurm
done
