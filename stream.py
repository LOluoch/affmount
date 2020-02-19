#!/usr/bin/env python3
import sys
import os
import argparse
from pyaff4 import container
from pyaff4 import aff4_image
import hexdump

def GetImgInfoObjectForAff4(path):
    aff4_stream = container.Container.open(path)
    streamsize = aff4_map_stream.
    buf = aff4_stream.Read(4096) #Chunk length
    total_buf+=buf
    print(hexdump.hexdump(buf))


#Program execution starts here
def main(): 
    if len(sys.argv) < 2:
        sys.exit("No file provided")
    else:
        GetImgInfoObjectForAff4(sys.argv[1])       



if __name__ == "__main__":
    main()