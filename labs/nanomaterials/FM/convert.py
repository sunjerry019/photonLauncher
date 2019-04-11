#!/usr/bin/env python3

import csv
import json

data = dict()

with open('power.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["FM"] not in data:
            data[row["FM"]] = dict()

        if row["SD Label"] not in data[row["FM"]]:
            data[row["FM"]][row["SD Label"]] = dict()

        if row["Lens"] not in data[row["FM"]][row["SD Label"]]:
            data[row["FM"]][row["SD Label"]][row["Lens"]] = dict()

        if row["Type"] not in data[row["FM"]][row["SD Label"]][row["Lens"]]:
            data[row["FM"]][row["SD Label"]][row["Lens"]][row["Type"]] = dict()

        data[row["FM"]][row["SD Label"]][row["Lens"]][row["Type"]][row["Lamp"]] = row["Power/mW"]

with open('power.json', 'w') as f:
    f.write(json.dumps(data))
