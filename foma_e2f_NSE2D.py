#!/usr/bin/python3

import sys
import argparse
import json
import os

from createParser import createParser

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    #print(path)
    with open(path+"/foma_e2f_NSE2D.json", "r") as fd:
        data = json.loads(fd.read())
    #print(data.keys())
    pr, kl = createParser(data)
    #print(kl)
    opt = pr.parse_args()
    optD = opt.__dict__
    print(optD)
    
    os.system("cat {} > main.fix.e2f.ini".format(optD['main']))
    os.system("cat {} > NSE.2D.fix.e2f.ini".format(optD['NSE2D']))
