import pandas as pd
import matplotlib.pyplot as plt

data = pd.DataFrame(columns=(
    "file",
    "name",
    "n",
    "m",
    "contracted_n",
    "contracted_m",
    "scc_n",
    "scc_m",
    "num_cycles",
    "max_cycle_size",
    "max_cycle_routings_found",
    "found_k"))

f = open("stats_clean.txt", "r")
print("Building data frame...\n")
for i, line in enumerate(f):
    # print("\n" + line.strip())
    line = line.split(",")
    file = line[0]
    name = line[1]
    n = int(line[2])
    m = int(line[3])
    contracted_n = int(line[4])
    contracted_m = int(line[5])
    scc_n = int(line[6])
    scc_m = int(line[7])
    num_cycles = int(line[8])
    cycle_indices = list(range(9, 9 + int(num_cycles)))
    max_cycle_size = 0
    for index in cycle_indices:
        max_cycle_size = max(max_cycle_size, int(line[index]))
    found_k = int(line[-1])
    line = line[index + 1:-1]
    scc_routings_tried = len(line)
    max_cycle_routings_found = 0
    for item in line:
        max_cycle_routings_found = max(max_cycle_routings_found, int(item))
    data.loc[i] = [file, name, n, m, contracted_n, contracted_m, scc_n, scc_m,
                   num_cycles, max_cycle_size,
                   max_cycle_routings_found, found_k]
f.close()

for column_name in ["n", "m", "contracted_n", "contracted_m", "scc_n", "scc_m",
                    "num_cycles", "max_cycle_size", "max_cycle_routings_found",
                    "found_k"]:
    data[column_name] = pd.to_numeric(data[column_name])

data.to_csv("stats_df.csv", index=False)

print("Counts of found k:")
print(data.groupby("found_k").count()["n"])

# hist = data[data["found_k"] > 0].hist("max_cycle_routings_found")
# plt.show()

print(data[data["found_k"] > 0]["max_cycle_routings_found"].max())

print(data[(data["found_k"] == 0) & (data["max_cycle_routings_found"] <
                                     10000000)][["name",
                                                "max_cycle_routings_found"]])
