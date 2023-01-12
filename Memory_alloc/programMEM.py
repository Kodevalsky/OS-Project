
import json as js

import copy as cp

import numpy as np 

import matplotlib.pyplot as plt


pathToList = "list.txt"

with open("/home/kovalsky/Coding/so_project/Memory_alloc/configs.json", 'r') as config:
    confVals = js.load(config)

tpf_fifo = [[] for i in range(0,len(confVals["config_data"]["amount_of_frames"]))]

tpf_lru = [[] for i in range(0,len(confVals["config_data"]["amount_of_frames"]))]

refs_data = [[] for i in range(0,confVals["config_data"]["amount_of_series"])]

def readProcessList(list):
    number = 0

    with open(list, 'r') as refs:
        for line in refs:

            if line == "\n":
                number += 1
                continue

            refs_data[number].append(int(line))

def setSimulation(func, tpf, copy):
    for val in range(0,len(confVals["config_data"]["amount_of_frames"])):
        for i in range(0,confVals["config_data"]["amount_of_series"]):
            print("Attempting a simluation...")
            tpf[val].append(func(copy[i], val))


def fifo(refs_series, frameVal):
    queue_size = confVals["config_data"]["amount_of_frames"][frameVal]
    faults = 0
    queue_counter = 0
    refs_counter = 0
    queue = []
    while refs_counter < confVals["config_data"]["amount_of_refs"]:
        if refs_series[refs_counter] in queue:
            print("No fault occured!")
            pass
        elif refs_series[refs_counter] not in queue:
            if len(queue) < queue_size:
                queue.append(refs_series[refs_counter])
                faults += 1
                print("A fault occured!")
            else:
                queue[queue_counter % queue_size] = refs_series[refs_counter]
                queue_counter +=1
                faults += 1
                print("A fault occured!")
        refs_counter += 1
    return faults

def lru(refs_series, framelVal):
    queue_size = confVals["config_data"]["amount_of_frames"][framelVal]
    faults = 0
    queue_counter = 0
    refs_counter = 0
    queue = []
    lru_queue = []
    while refs_counter < confVals["config_data"]["amount_of_refs"]:
        if refs_series[refs_counter] in queue:
            print("No fault occured!")
            if refs_series[refs_counter] in lru_queue:
                del lru_queue[lru_queue.index(refs_series[refs_counter])]
            lru_queue.append(refs_series[refs_counter])
            pass
        elif refs_series[refs_counter] not in queue:
            if len(queue) < queue_size:
                queue.append(refs_series[refs_counter])
                lru_queue.append(refs_series[refs_counter])
                faults += 1
                print("A fault occured!")
            else:
                queue[queue.index(lru_queue[0])] = refs_series[refs_counter]
                del lru_queue[0]
                lru_queue.append(refs_series[refs_counter])
                faults += 1
                print("A fault occured!")
        refs_counter += 1
    return faults



def getStats(data, name):
    tab = {}
    tab[name] = {}
    tab[name]["std_dev"] = np.std(data)
    tab[name]["total_mean"] = np.mean(data)
    tab[name]["max_faults"] = max(data)
    tab[name]["raw_values"] = data

    with open("stats"+name+".json", 'w') as file:
        js.dump(tab, file)

    a, plot = plt.subplots()
    plot.hist(data, color=['green', 'yellow', 'blue'])
    plot.set(title = "The values of faults in each series",\
            xlabel = "The amount of faults",\
            ylabel = "The amount of series where a given amount of faults happened")

    plot.grid()
    filename = "Plot_"+name+"_"\
        +str(confVals["config_data"]["amount_of_refs"])+"_"\
        +str(confVals["config_data"]["amount_of_series"])+"_"\
        +str(confVals["config_data"]["amount_of_pages"])+"_"\
        +".png"
    plt.savefig(filename)
    plt.show()

readProcessList(pathToList)

copy = cp.deepcopy(refs_data)
copy2 = cp.deepcopy(refs_data)


setSimulation(fifo, tpf_fifo, copy)
setSimulation(lru, tpf_lru, copy2)

getStats(tpf_fifo, "fifo")
getStats(tpf_lru, "lru")
