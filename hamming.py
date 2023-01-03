#!env python

import math
from copy import deepcopy
from functools import reduce
from operator import ixor

class binary_number:

    def __init__(self, data, length=None):
        self.binary = []
        bs = bin(data)[2:]
        if length:
            while length > len(bs):
                self.binary.append(0)
                length -= 1
        for b in bs:
            self.binary.append(int(b))

    def __str__(self):
        return str(self.binary)

    def __len__(self):
        return len(self.binary)

    def __int__(self):
        combined_binary_string = '0b'
        for b in self.binary:
            combined_binary_string += str(b)
        return int(combined_binary_string, 2)

    def insert_at(self, bit, pos):
        if pos > len(self.binary):
            return
        head = self.binary[:(pos-1)]
        tail = self.binary[(pos-1):]
        self.binary = head + [bit] + tail

    def get_one_bits(self):
        array_of_positions = []
        pos = 1
        for b in self.binary:
            if (b == 1):
                array_of_positions.append(pos)
            pos += 1
        return array_of_positions

def hamming_distance(w1, w2):
    return (bin(w1 ^ w2)[2:]).count('1')

def hamming_distance_code(code):
    min_distance = None
    for w1_pos in range(0, len(code)):
        for w2_pos in range(w1_pos+1, len(code)):
            d = hamming_distance(code[w1_pos], code[w2_pos])
            if (min_distance == None) or (d < min_distance):
                min_distance = d

    return min_distance

def hamming_code(data, length=None):
    bdata = binary_number(data, length)
    required_parity_bits = math.ceil(math.log2(len(bdata))) + 1
    for p in range(required_parity_bits):
        bdata.insert_at('?', int(math.pow(2, p)))

    #print("Found parity bits at %s" % bdata.get_one_bits())
    one_bits = bdata.get_one_bits()
    if len(one_bits) > 0:
        xor_result = reduce(ixor, one_bits)
    else:
        xor_result = 0
    parity_bits = binary_number(xor_result, required_parity_bits)
    bidx = 0
    pidx = 0
    for b in bdata.binary:
        if (b == '?'):
            bdata.binary[bidx] = parity_bits.binary[pidx]
            pidx += 1
        bidx += 1
    return bdata

if __name__ == '__main__':

    code = []
    for w1 in range(0,256):
        bw1 = binary_number(w1, 8)
        hc = hamming_code(w1, 8)
        print("Hamming code for %s is %s" % (bw1, hc))
        code.append(int(hc))

    print("Hamming distance for %s is %i" % (code, hamming_distance_code(code)))
