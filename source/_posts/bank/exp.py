from pwnlib.tubes.remote import remote

def sxor(s1, s2):
    return ''.join(chr(ord(a)^ord(b)) for a, b in zip(s1, s2))

def falsify(hashcode):
    key = sxor('TRANSACTION: 1000', hashcode.decode('hex'))
    return sxor('TRANSACTION:99999', key).encode('hex')


r = remote('188.166.133.53', 10061)

for i in range(20):
    print r.recvuntil('Command: ')
    r.sendline('create 1000')

    line = r.recvline()
    print line
    hashcode = line.split()[-1]

    print r.recvuntil('Command: ')
    r.sendline('complete ' + str(i) + ' ' + falsify(hashcode))

print r.recvuntil('Command: ')
