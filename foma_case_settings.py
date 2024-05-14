#!/usr/bin/env python3
import time
import os
from Egorych2FomaArgParser import Egorych2FomaArgParser

# list of foma configs to update
# TODO: read from 'upload' gui nodes
FOMA_CONFIGS = ["main.ini", "NSE.2D.ini"]

def prepareIniFiles():
    if not os.path.exists("settings"):
        os.makedirs("settings")
 
    path1 = "main.fix.ini"
    path2 = "settings/main.ini"
    print("Moving {} to {}".format(path1, path2))
    with open(path1, "r") as fin, open(path2, "w+") as fout:
        lines = fin.readlines()
        # trim first line with [SECTION0] fix   
        fout.writelines(lines[1:]) 
       
    path1 = "NSE.2D.fix.ini"
    path2 = "settings/NSE.2D.ini"
    print("Moving {} to {}".format(path1, path2))
    with open(path1, "r") as fin, open(path2, "w+") as fout:
        lines = fin.readlines()
        fout.writelines(lines[:]) 


# this script is invoked from gui exec node
if __name__ == '__main__':
    
    e2f = Egorych2FomaArgParser()
    
    e2f.parseEgorychNodeArgs("foma_case_settings.json")
    
    for fcfg in FOMA_CONFIGS:
        e2f.updateFomaConfig(fcfg)
    
    prepareIniFiles()

