import re, zlib

def byteswap(s):
    s = re.findall('..', s)
    return ''.join(list(reversed(s)))

def crc32b(s):
    h = format(zlib.crc32(bytes(s, 'utf-8')), 'x')
    return h

print(byteswap(crc32b(input('Enter a parameter name: '))))
