#!/usr/bin/env python3

import random as rd
import json as js

pathToList = "list.txt"

with open("config.json", 'r') as config:
    confVals = js.load(config)

rd.seed(confVals["config_data"]["random_seed"])

with open(pathToList, 'w') as file:
    for i in range(0,confVals["config_data"]["amount_of_series"]):
        for x in range(0, confVals["config_data"]["amount_of_proc"]):
            line = str(rd.randint(0,confVals["config_data"]["max_await"])) + ',' +  str(rd.randint(1,confVals["config_data"]["max_exec"]))
            file.write(line + '\n')
        file.write("\n")