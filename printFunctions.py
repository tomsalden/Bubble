# Several functions to print the current outputs of the system
import os

def clearPrints():
    os.system('clear')

def printHeadPosition(headPosition):
    filename = str(str(headPosition[0])+str(headPosition[1])+str(headPosition[2])+".txt")
    f = open("Visuals/" + filestring,'r')
    file_contents = f.read()
    print(file_contents)
