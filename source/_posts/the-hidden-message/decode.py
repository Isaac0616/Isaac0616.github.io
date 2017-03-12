from base64 import b64decode

with open('README.TXT') as f:
    lines = f.read().split('\n')

string = ''
for l in lines[:-2]:
    for byte in l.split()[1:]:
        string += chr(int(byte, 8))

print 'octal to ASCII:'
print repr(string)
print
print 'base64 decode:'
print repr(b64decode(string))
