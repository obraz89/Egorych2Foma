#!/usr/bin/env python3

import os
import time

def runApp(exe):
    start = time.perf_counter()
    out = os.system(exe)
    #out = subprocess.check_output([exe], encoding = 'utf-8')
    duration = time.perf_counter() - start
    return{'out':out, 'duration':duration}

def runCaseLocal():
    #TODO: foma executable placement
    FOMA_DIR = "/opt/foma/FOMA/bin-gcc485"
    cmd1 = "export FOMA={};".format(FOMA_DIR)
    cmd2 = FOMA_DIR+"/foma . -l log.txt;"
    runApp(cmd1+cmd2)

        
if __name__ == '__main__':
    runCaseLocal()
    print("Foma.py: sleeping for 50s")
    time.sleep(50)
