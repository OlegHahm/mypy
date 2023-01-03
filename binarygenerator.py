#!env python

if __name__ == '__main__':
    for i in range(256):
#        print("\\item \\verb!%3i -- %08s" % (i, bin(i)[2:]))
        print("\\item \\verb!{:3} -- {:08b}!".format(i, i))
