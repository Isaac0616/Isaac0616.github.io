from sympy import nextprime
from pwnlib.tubes.remote import remote

r = remote('188.166.133.53', 11059)

while True:
    lines = r.recvlines(2)
    print '\n'.join(lines)
    p = nextprime(lines[1].split()[8][:-1])
    print p
    r.send(str(p))
