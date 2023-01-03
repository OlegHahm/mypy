#!env python
import sys

class ipv4_addr():
    def __init__(self, string_repr):
        octets = string_repr.split('.')
        if len(octets) != 4:
            raise ValueError
        self.octets = []
        for s in octets:
            self.octets.append(int(s))

def subnet_match(sender_addr, receiver_addr, subnet):
    sa = ipv4_addr(sender_addr)
    da = ipv4_addr(receiver_addr)
    sn = ipv4_addr(subnet)

    for i in range(4):
        if (sa.octets[i] & sn.octets[i]) != (da.octets[i] & sn.octets[i]):
            print("Mismatch: %i and %i" % (sa.octets[i], da.octets[i]))
            return False

    return True

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Usage: %s <SENDER> <RECEIVER> <SUBNET>" % sys.argv[0])
        sys.exit(1)
    if not subnet_match(sys.argv[1], sys.argv[2], sys.argv[3]):
        result = "not "
    else:
        result = ""

    print("%s and %s are %sin the same subnet" % (sys.argv[1], sys.argv[2], result))
