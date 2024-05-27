#!/usr/bin/env python3

import sys
import os
import configparser as cp
import json
import re

# TODO: testing with hisa, replace with foma_config.json
ARGS_JSON="hisa.json"

from createParser import createParser

class Egorych2FomaArgParser:

    def __init__(self):
        # config parser
        self.cp = None
        
        # current file for config parser
        self.cp_file = None
        
        # args passed from egorych gui node
        self.args = None
        
    # in foma config first option can be without section
    # append section name for them and assume that after 
    # all options are inside sections
    def StripIniExtension(self, fn):
        pts = fn.split(".")
        if (len(pts)<2):
            print("Error: bad ini name, must be smth.ini")
        return ".".join(pts[:-1])

    def fixFomaConfig(self, foma_config, foma_config_fixed=""): 
        _SECT_TMPL=r"""
        \[                                 # [
        (?P<header>[^]]+)                  # very permissive!
        \]                                 # ]
        """
        COMM_PREFIX="#"
        self.SECTCRE = re.compile(_SECT_TMPL, re.VERBOSE)
        
        if (not foma_config_fixed):
            foma_config_fixed = self.StripIniExtension(foma_config)+".fix.ini" 
        
        with open(foma_config) as fc, open(foma_config_fixed, "w") as f2e:
        
            no_section_read = True
            for lineno, line in enumerate(fc, start=1):
                if(line.strip().startswith(COMM_PREFIX)):
                    f2e.write(line)
                    continue
                mo = self.SECTCRE.match(line.strip())
                if mo:
                    f2e.write(line)
                    no_section_read = False
                else:
                    if (no_section_read):
                        f2e.write("[SECTION0]\n")
                        f2e.write(line)
                        no_section_read = False
                    else:
                        f2e.write(line)
                        
        return foma_config_fixed
    
    def makeE2FConfig(self, foma_config, e2f_config=""):
    
        config = cp.ConfigParser()
        # read-write sections & options case sensitive
        config.optionxform = str
        config.read(foma_config)
        
        # erase values
        for section in config.sections():
            for option in config.options(section):
                config.set(section, option, "")
        
        if (e2f_config==""):
            parts = foma_config.split(".")
            parts.insert(-1, "e2f")
            e2f_config=".".join(parts)
            
        with open(e2f_config, "w+") as e2fp:
            config.write(e2fp)
        
    
    def loadE2FConfig(self, e2f_config):
        self.cp = cp.ConfigParser()
        # read-write sections & options case sensitive
        self.cp.optionxform = str
        
        self.cp_file = e2f_config
        
        if (os.path.isfile(e2f_config)):
            self.cp.read(e2f_config)
        else:
            print("E2F warning: config {e2f_config} not found, making".format(e2f_config=e2f_config))
            self.makeE2FConfig("", e2f_config)
    
    # update single option in e2f config
    def updateE2FOption(self, e2f_cfg_file, section, option, value):
        if (self.cp_file!=e2f_cfg_file):
            self.loadE2FConfig(e2f_cfg_file)
        
        self.cp.set(section, option, value)
        with open(e2f_cfg_file, "w+") as e2fp:
            self.cp.write(e2fp)
    
    def parseEgorychNodeArgs(self, args_json):
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        #print(path)
        with open(path+"/"+args_json, "r") as fd:
             data = json.loads(fd.read())
        #print(data.keys())
        pr, kl = createParser(data)
        #print(kl)
        self.args = pr.parse_args()
        optD = self.args.__dict__
    
    def getArg(self, arg):
        val = str(self.args.__dict__.get(arg, ""))
        if (val==""): 
            print("e2f error: arg={} not found in arg list".format(arg))
        return val
    
    # update static parameters in foma config
    # read static param <=> arg match from e2f config
    # update corresponding static param in foma config with provided arg value
    def updateFomaConfig(self, foma_config):
        # using default e2f config
        e2f_fn = self.StripIniExtension(foma_config)+".fix.e2f.ini"
        
        print("e2f:Loading e2f config {}".format(e2f_fn))
        self.loadE2FConfig(e2f_fn)
        
        foma_cp = cp.ConfigParser()
        # read-write sections & options case sensitive
        foma_cp.optionxform = str
        
        foma_config_fixed = self.StripIniExtension(foma_config)+".fix.ini"
        foma_cp.read(foma_config_fixed)
        
        scp = self.cp
        
        for section in scp.sections():
            #debug, check sections
            #print("e2f: section={}".format(section))
            for option in scp.options(section):
                arg = scp.get(section, option)
                if (arg): 
                    val = str(self.args.__dict__.get(arg, ""))
                    if val:
                        foma_cp.set(section, option, val)
                    else:
                        print("E2F: warning: opt is in e2f but not given by egorych: {}".format(arg))
    
        
        print("e2f: Saving updated config {}".format(foma_config_fixed))
        with open(foma_config_fixed, "w") as fc:
            foma_cp.write(fc)
    
    # update bc sections for a known list of bc types
    # update corresponding sections with provided arg values
    def updateFomaConfigBC(self, foma_config):
        # using default e2f config
        e2f_fn = self.StripIniExtension(foma_config)+".fix.e2f.ini"
        
        print("e2f:Loading e2f config {}".format(e2f_fn))
        self.loadE2FConfig(e2f_fn)
        
        foma_cp = cp.ConfigParser()
        # read-write sections & options case sensitive
        foma_cp.optionxform = str
        
        foma_config_fixed = self.StripIniExtension(foma_config)+".fix.ini"
        foma_cp.read(foma_config_fixed)
        
        scp = self.cp
        
        #update boundary section
        section = "NSE.2D/boundary"
        option = self.getArg("GridPatchName")
        val = self.getArg("BCType")
        foma_cp.set(section, option, val)
        
        # update "NSE.2D-{BCType}/{GridPatchName}" with args
        # leave only args for this section 
        kf = list(self.args.__dict__.keys())
        for k in ["GridPatchName", "BCType"]:
          kf.remove(k)
        
        section = "NSE.2D-{BCType}/{PatchName}".format(BCType=val, PatchName=option)
        for k in kf:
          foma_cp.set(section, k, self.getArg(k))
        
        with open(foma_config_fixed, "w") as fc:
            foma_cp.write(fc)


if __name__ == '__main__':
    
    e2f = Egorych2FomaArgParser()
    
    e2f.parseEgorychNodeArgs()
    
    e2f.fixFomaConfig("main.ini", "main.fix.ini")
    
    e2f.makeE2FConfig("main.fix.ini")

    config = cp.ConfigParser()
    # read-write sections & options case sensitive
    config.optionxform = str
    config.read('main.fix.ini')
    print(config.sections())
    
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    #print(path)
    with open(path+"/hisa.json", "r") as fd:
        data = json.loads(fd.read())
    #print(data.keys())
    pr, kl = createParser(data)
    #print(kl)
    opt = pr.parse_args()
    optD = opt.__dict__
    print("Argparse:")
    print(opt)
    print("KeyList:")
    print(kl)
    print(f"Mach={opt.Mach}")
    print("Config parser location:")
    print(cp.__file__)
    print("Options in section init")
    print(config.options("init"))