import subprocess


# for each of fpt file and heur file
# read each id, get its mem, save in list.
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
