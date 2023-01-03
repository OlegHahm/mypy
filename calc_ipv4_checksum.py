#!env python

import sys

if __name__ == '__main__':

    chksum = 0
    for arg in sys.argv[1:]:
        print("Adding %s (%s) to %s (%s)" % (bin(int(arg, 16)), arg, bin(chksum), hex(chksum)))
        chksum += int(arg, 16)
        if len(bin(chksum)) > 18:
            chksum -= 0x10000
            chksum += 1

    print("Sum is      %18s (%s)" % (bin(chksum), hex(chksum)))
    chksum ^= 0xffff
    print("Checksum is %18s (%s)" % (bin(chksum), hex(chksum)))

