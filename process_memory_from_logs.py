import subprocess


# for each of fpt file and heur file
# read each id, get its mem, save in list.
# command is sacct --user=p19t655 -S 2021-04-18
jobs = subprocess.check_output(['sacct', '--user=p19t655', '-S', '2021-04-18',
'--format=JobID,JobName%30,State'])
lines = jobs.split()[6:]
heur_counts = 0
fpt_counts = 0
heur_min = 1000
heur_max = 0
heur_total = 0
fpt_min = 1000
fpt_max = 0
fpt_total = 0
# each job takes up 6 elements
for job_index in range(0, len(lines), 6):
    job_id = lines[job_index].decode('ascii')
    job_name = lines[job_index + 1].decode('ascii')
    status = lines[job_index + 2].decode('ascii')
    if "run_fpt" in job_name and status == "COMPLETED":
        mem_info = subprocess.check_output(['sacct', '-j', job_id, '--format=MaxRSS']).decode('ascii').split()[2]
        if mem_info[-1] == "K":
            # in kb. divide by 1000
            memory = int(mem_info[:-1])/1000
        if mem_info[-1] == "M":
            memory = float(mem_info[:-1])
        fpt_min = min(memory, fpt_min)
        fpt_max = max(memory, fpt_max)
        fpt_total += memory
    if "run_fpt" in job_name:
        fpt_counts += 1
    if "run_heuristic" in job_name:
        assert status == "COMPLETED"
        heur_counts += 1
        mem_info = subprocess.check_output(['sacct', '-j', job_id, '--format=MaxRSS']).decode('ascii').split()[2]
        if mem_info[-1] == "K":
            # in kb. divide by 1000
            memory = int(mem_info[:-1])/1000
        if mem_info[-1] == "M":
            memory = float(mem_info[:-1])
        heur_min = min(memory, heur_min)
        heur_max = max(memory, heur_max)
        heur_total += memory
    print(job_id, job_name, status)
    print("RSS:", memory)

print("total heur:", heur_counts)
print("avg:", heur_total/heur_counts)
print("min:", heur_min)
print("max:", heur_max)
print("total fpt:", fpt_counts)
print("avg:", fpt_total/fpt_counts)
print("min:", fpt_min)
print("max:", fpt_max)

"""
heur_maxrss = []
fpt_maxrss = []
heur_maxvm = []
fpt_maxvm = []
for id_file in ["fpt_ids.txt", "heur_ids.txt"]:
    f = open(id_file, "r")
    for line in f:
        if line[0] == "S":
            job_id = line.strip().split()[-1]
            mem_info = subprocess.check_output(['sacct', '-j', job_id,
'--format=MaxRSS,MaxVMSize'])
            try:
                intmaxrss = int(mem_info.split()[-2][:-1])
                intmaxvmsize = int(mem_info.split()[-1][:-1])
            except ValueError:
                pass 
            if id_file == "fpt_ids.txt":
                fpt_maxrss.append(intmaxrss)
                fpt_maxvm.append(intmaxvmsize)
            else:
                heur_maxrss.append(intmaxrss)
                heur_maxvm.append(intmaxvmsize)
    f.close()

print("max heur rss", max(heur_maxrss)/1000)
print("max fpt rss", max(fpt_maxrss)/1000)
print("max heur vm", max(heur_maxvm)/1000)
print("max fpt vm", max(fpt_maxvm)/1000)

print("min heur rss", min(heur_maxrss)/1000)
print("min fpt rss", min(fpt_maxrss)/1000)
print("min heur vm", min(heur_maxvm)/1000)
print("min fpt vm", min(fpt_maxvm)/1000)

print("avg heur rss", (sum(heur_maxrss)/len(heur_maxrss))/1000)
print("avg fpt rss", (sum(fpt_maxrss)/len(fpt_maxrss))/1000)
print("avg heur vm", (sum(heur_maxvm)/len(heur_maxvm))/1000)
print("avg fpt vm", (sum(fpt_maxvm)/len(fpt_maxvm))/1000)

# full data 
print("heur maxrss")
print(heur_maxrss)
print("fpt maxrss")
print(fpt_maxrss)
print("heur maxvm")
print(heur_maxvm)
print("fpt maxvm")
print(fpt_maxvm)
"""
