#!/usr/bin/env python3

import random as rd
import json as js
import os

def generateRefs(**kwargs):
    pathToList = kwargs['path']

    with open(os.path.dirname(os.path.realpath(__file__)) + "/configs.json", 'r') as config:
        confVals = js.load(config)

    rd.seed(confVals["config_data"]["random_seed"])

    with open(pathToList, 'w') as file:
        for i in range(0,confVals["config_data"]["amount_of_series"]):
            for x in range(0, confVals["config_data"]["amount_of_refs"]):
                line = str(rd.randint(0,confVals["config_data"]["amount_of_pages"]))
                file.write(line + '\n')
            file.write("\n")