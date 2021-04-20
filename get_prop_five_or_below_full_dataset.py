# walk through every instance in the original truth files, and count nontrivial
# instances and nontrivial instances with 5 or fewer paths.

from pathlib import Path

total = 0
five_or_fewer = 0

truth_dir = Path("basic_instances")
filenames = list(filter(Path.is_file, truth_dir.glob('**/*.truth')))
for f in filenames:
    with open(f, "r") as fo:
        line = fo.readline()
        first_line = True
        k = 0
        while line:
            line = fo.readline()
            if line and line[0] == "#":
                if not first_line and k > 1:
                    total += 1
                if k <= 5 and k > 1:
                    five_or_fewer += 1
                first_line = False
                k = 0
            else:
                k += 1

print(five_or_fewer/total)
