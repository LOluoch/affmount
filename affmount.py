#!/usr/bin/env python3
import sys
import os
import argparse
from pyaff4 import container
from pyaff4 import aff4_image

# Open the AFF4 volume 
def extractStream(path,dirpath):
    if os.path.exists(path):
        aff4_map_stream = container.Container.open(path)
        with open(os.path.join(dirpath,"stream"),"wb") as output:
            try:
                data = aff4_map_stream.read()
                output.write(data)
            except NameError:
                pass
            
    else:
        sys.exit("File does not exist")

#Program execution starts here
def main(): 
    if len(sys.argv) < 2:
        sys.exit("No file provided.")
    elif len(sys.argv) < 3:
        sys.exit("No output directory specified.")
    else:
        extractStream(sys.argv[1],sys.argv[2])       



if __name__ == "__main__":
    main()