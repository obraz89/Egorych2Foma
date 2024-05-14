#!/usr/bin/python3

import sys
import argparse
import json
import os

from createParser import createParser
from Egorych2FomaArgParser import Egorych2FomaArgParser

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    #print(path)
    with open(path+"/foma_ini_NSE2D.json", "r") as fd:
        data = json.loads(fd.read())
    #print(data.keys())
    pr, kl = createParser(data)
    #print(kl)
    opt = pr.parse_args()
    optD = opt.__dict__
    print(optD)
    
    e2f = Egorych2FomaArgParser()
    
    e2f.fixFomaConfig(optD['main'], "main.fix.ini")
    e2f.fixFomaConfig(optD['NSE2D'], "NSE.2D.fix.ini")
