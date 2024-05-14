#!/usr/bin/env python3

import sys
import argparse
import os
from createParser import createParser

if __name__ == '__main__':
    
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    print(sys.argv[0])
    return
    with open(path+"/hisa.json", "r") as fd:
        data = json.loads(fd.read())
    #print(data.keys())
    pr, kl = createParser(data)
    #print(kl)
    opt = pr.parse_args()
    optD = opt.__dict__
