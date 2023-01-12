#!/usr/bin/env python3

# CPU Time allocation simulation program 

# Importing needed libraries

import numpy as np 

import matplotlib.pyplot as plt

import json as js

import copy as cp

# Setting a path to a .txt file containing a list of processes

pathToList = "list.txt"

# Opening a .json file with configurational arguments

with open("config.json", 'r') as config:
    confVals = js.load(config)

# Creating a dictionary with keys as a number of series and value being a list of Process-class objects

processSequence = [[] for i in range(0,confVals["config_data"]["amount_of_series"])]

# Creating lists to hold the effects of our simulations

tteTotal_fcfs = [[] for i in range(0,confVals["config_data"]["amount_of_series"])]

tteTotal_sjf = [[] for i in range(0,confVals["config_data"]["amount_of_series"])]


# Defining a Process class which simulates an actual process

class Process:
    def __init__(self, processAwait, processTime):
        self.awaitTime  = processAwait
        self.execTime = processTime
        self.completion = False
        self.timeToExec = 0

# Function for reading a .txt list of processes

def readProcessList(list):
    number = 0

    with open(list, 'r') as processes:

        for line in processes:

            if line == "\n":
                number += 1
                continue

            values = line.split(",")
            procObj = Process(int(values[0]), int(values[1]))
            processSequence[number].append(procObj)

    for i in range(0, confVals["config_data"]["amount_of_series"]):
        processSequence[i].sort(key=lambda x: x.awaitTime)

# Implementation of the fcfs algorithm

def fcfs(storage, timeToExecTable):

    timer = 0
    queue = []

    while any(element.completion == False for element in storage) or queue:

        for proc in storage:

            if proc.awaitTime == timer:
                print("Adding process to CPU queue")
                queue.append(proc)
                proc.completion = True

        if queue:
            queue[1:].sort(key=lambda x: x.execTime)
            
            if queue[0].execTime == 0:
                print("Process completed time to execute was: " + str(queue[0].timeToExec))
                timeToExecTable.append(queue[0].timeToExec)
                del queue[0]
        
            elif queue[0]:
                print("Executing process...")
                queue[0].execTime -= 1

        for element in queue[1:]:
                element.timeToExec += 1

        timer += 1

# Implementation of the SJF algorithm

def sjf(storage, timeToExecTable):
    timer = 0
    queue = []

    while any(element.completion == False for element in storage) or queue:

        for proc in storage:

            if proc.awaitTime == timer:
                print("Adding process to CPU queue")
                queue.append(proc)
                proc.completion = True
        
        queue.sort(key = lambda x: x.execTime)

        if queue:

            if queue[0].execTime == 0:
                print("Process completed time to execute was: " + str(queue[0].timeToExec))
                timeToExecTable.append(queue[0].timeToExec)
                del queue[0]
        
            elif queue[0]:
                print("Executing process...")
                queue[0].execTime -= 1

        for element in queue[1:]:
                element.timeToExec += 1

        timer += 1

# Function for getting the algorithm running a specified number of times

def setSimulation(func, tte, proCopy):
    for i in range(0,confVals["config_data"]["amount_of_series"]):
        func(proCopy[i], tte[i])

# A function preparing statistics and plotting the effects of the simulations

def getStats(tte, name):
    means = []

    for sample in tte:
        mn = np.mean(sample)
        means.append(mn)

    a, plot = plt.subplots()
    plot.hist(means, color='orange')
    plot.set(title = "The means of each series of calculations",\
            xlabel = "Waittime for CPU",\
            ylabel = "Amount of processes")

    plot.grid()

    filename = "Plot_"+name+"_"\
        +str(confVals["config_data"]["amount_of_series"])+"_"\
        +str(confVals["config_data"]["amount_of_proc"])+"_"\
        +str(confVals["config_data"]["max_await"])+"_"\
        +".png"

    plt.savefig(filename)
    plt.show()

    tab = {}
    tab[name] = {}
    tab[name]["std_dev"] = np.std(means)
    tab[name]["total_mean"] = np.mean(means)
    tab[name]["max_exec_wait"] = max(means)
    tab[name]["raw_values"] = means

    with open("stats" + name + ".json", "w") as statFile:
        js.dump(tab, statFile)

# Main part of the program

if __name__ == "__main__":

    # Reading the file with collections of process values

    readProcessList(pathToList)

    # Creating copies of the list to pass into setSimulation() function

    proCopy1 = cp.deepcopy(processSequence)
    proCopy2 = cp.deepcopy(processSequence)

    # Calling the simulation function for FCFS

    setSimulation(fcfs, tteTotal_fcfs, proCopy1)

    # Calling the simulation function for SJF

    setSimulation(sjf, tteTotal_sjf, proCopy2)

    # Calling the stats function for both scores

    getStats(tteTotal_fcfs, "fcfs")
    getStats(tteTotal_sjf, "sjf")