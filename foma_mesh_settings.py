#!/usr/bin/env python3

import os
from Egorych2FomaArgParser import Egorych2FomaArgParser

# list of foma configs to update
FOMA_CONFIGS = ["main.ini"]

if __name__ == '__main__':
    
    e2f = Egorych2FomaArgParser()
    
    e2f.parseEgorychNodeArgs("foma_mesh_settings.json")
    
    grd = e2f.args.__dict__['mesh']
    os.system("ln -s {} grid.cgns".format(grd))
    
    #for fcfg in FOMA_CONFIGS:
    #    e2f.updateFomaConfig(fcfg)

