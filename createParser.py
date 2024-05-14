#!/usr/bin/python3

import sys
import argparse
import json

def createParser (data):
    parser = argparse.ArgumentParser()
    keyList = []
    for key in data.keys():
       if 'option' in data[key]:
           #print(data[key])
           option = data[key]['option']
           keyList.append(option)
           if not option.startswith('-'):
               option = '-'+option
           if 'default' in data[key].keys():
               default = data[key]['default']
           else:
               default = None
           parser.add_argument (option, default=default, help=data[key]['discription'])
    for inp in data['inputs']:
        if 'option' in data['inputs'][inp]:
            keyList.append(data['inputs'][inp]['option'])
            fileType = 'everyone'
            if 'fileType' in data['inputs'][inp].keys():
                fileType = data['inputs'][inp]['fileType']

            parser.add_argument(data['inputs'][inp]['option'], help=fileType+" file input")

    for out in data['outputs']:
        if 'option' in data['outputs'][out]:
            keyList.append(data['outputs'][out]['option'])
            fileType = 'everyone'
            if 'fileType' in data['outputs'][out].keys():
                fileType = data['outputs'][out]['fileType']

            parser.add_argument(data['outputs'][out]['option'], help=fileType+" file output")
    print(keyList)
    parser.add_argument('-settings', help='settings data', default=None)
    return parser, keyList

def main():
    #print(sys.argv)
    with open(sys.argv[1], "r") as fd:
        data = json.loads(fd.read())
    pr, kl = createParser(data)
    print(kl)
    print(pr)
    opt = pr.parse_args()

if __name__ == '__main__':
    main()
