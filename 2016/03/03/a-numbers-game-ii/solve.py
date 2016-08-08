from pwnlib.tubes.remote import remote

def decode(cypher):
    b = ''
    for c in cypher.split('.'):
        b += bin(ord(c)-51)[2:].rjust(2, '0')

    eq = ''
    for i in range(0, len(b), 8):
        eq += chr(int(b[i:i+8], 2)^32)

    return eq

def encode(eq):
    out = []
    for c in eq:
        q = bin(ord(c)^(2<<4)).lstrip("0b")
        q = "0" * ((2<<2)-len(q)) + q
        out.append(q)
    b = ''.join(out)
    pr = []
    for x in range(0,len(b),2):
        c = chr(int(b[x:x+2],2)+51)
        pr.append(c)
    s = '.'.join(pr)
    return s

r = remote('188.166.133.53', 11071)

while True:
    lines = r.recvlines(2)
    print '\n'.join(lines)

    eq = decode(lines[1].split()[2])
    print 'equation:', eq
    sp = eq.split()

    if sp[1] == '+':
        x = int(sp[4]) - int(sp[2])
    elif sp[1] == '-':
        x = int(sp[4]) + int(sp[2])
    elif sp[1] == '*':
        x = int(sp[4]) / int(sp[2])
    elif sp[1] == '/':
        x = int(sp[4]) * int(sp[2])

    print 'x = ', x
    print 'encode: ', encode(str(x))
    r.sendline(encode(str(x)))
