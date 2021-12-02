from pathlib import Path
from collections import defaultdict


output_dir = Path("run_memtest_err")
filenames = [str(f) for f in list(filter(Path.is_file, output_dir.glob('**/*')))]

max_ = 0
min_ = float("inf")
total = 0
count = 0
instances_over_100 = defaultdict(list)
for fn in filenames:
    with open(fn, "r") as f:
        for line in f.readlines():
            if line.split()[0].isnumeric():
                mem = int(line.split()[0])
                max_ = max(mem, max_)
                min_ = min(mem, min_)
                total += mem
                count += 1
                if mem/1024 > 100:
                    instance = fn.split(".err")[0].split("_")[-1]
                    instances_over_100[instance].append(round(mem/1024, 1))

print("min, max, average:")
print(f"{round(min_/1024,1)}, {round(max_/1024, 1)}, {round(total/1024/count, 1)}")
print(f"instances over 100 was {instances_over_100}")
print(f"count was {count} (should be 18207)")
                
