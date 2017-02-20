from pwn import *
from termcolor import colored
import re

context.log_level = 'error'

gdb_prompt = '\x01\x1b[1m\x1b[31m\x02pwndbg> \x01\x1b[0m\x1b[1m\x1b[0m\x02'
decrypted = []

# Launch the process and gdb. Then, dump the data after decryption.
for i in range(11):
    gdb = process(['gdb', '-q'])
    gdb.recvuntil(gdb_prompt, drop=True)

    meow = process('meow')
    gdb.sendline('attach ' + str(meow.proc.pid))
    gdb.recvuntil(gdb_prompt, drop=True)

    gdb.sendline('b *0x55555555568b')
    gdb.recvuntil(gdb_prompt, drop=True)

    key = bytearray('\x00'*10)
    if i != 0:
        key[i-1] = '\x01'
    meow.sendline(key)

    gdb.sendline('continue')
    gdb.recvuntil(gdb_prompt, drop=True)

    gdb.sendline('db $rdi 182')
    decrypted.append(re.findall(r'\b\S\S\b', gdb.recvuntil(gdb_prompt, drop=True)))

    gdb.close()
    meow.close()

# Compare the original data with data decrypted by differnt keys.
print '    0  1  2  3  4  5  6  7  8  9'
for i in range(len(decrypted[0])):
    print decrypted[0][i],
    for j in range(1, 11):
        if decrypted[0][i] != decrypted[j][i]:
            print colored(decrypted[j][i], 'red'),
        else:
            print decrypted[j][i],
    print ''
