#!/bin/bash  

rm -rf run_one_job_per_instance_err/
rm -rf run_one_job_per_instance_out/
rm -rf run_one_job_per_instance_slurms/
mkdir run_one_job_per_instance_err
mkdir run_one_job_per_instance_out
mkdir run_one_job_per_instance_slurms
    
for instance in $(seq 1999); do

echo "${instance}"
        
echo '#!/bin/bash
 
#SBATCH --job-name    '$instance'_mem_test        # job name
#SBATCH --output      run_one_job_per_instance_out/'$instance'.out # standard output file (%j = jobid)
#SBATCH --error       run_one_job_per_instance_err/'$instance'.err # standard error file
#SBATCH --partition   unsafe      # queue partition to run the job in
#SBATCH --nodes       1            # number of nodes to allocate
#SBATCH --ntasks-per-node 1        # number of descrete tasks - keep at one except for MPI 
#SBATCH --cpus-per-task=1          # number of CPU cores to allocate
#SBATCH --mem         1000         # 2000 MB of Memory allocated; set --mem with care
#SBATCH --time        2:00:00     # Maximum job run time
##SBATCH --mail-user   $email      # user to send emails to
##SBATCH --mail-type   ALL         # Email on: BEGIN, END, FAIL & REQUEUE
 
/usr/bin/time -f "%M" python ../coaster/coaster.py acyclic_sc_graph_instances/len4dem1subpaths4/graphs/sc0.graph --indices '$instance' --timeout 3600' > run_one_job_per_instance_slurms/"${instance}".slurm
sbatch run_one_job_per_instance_slurms/"${instance}".slurm
done
