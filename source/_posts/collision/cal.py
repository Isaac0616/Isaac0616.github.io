from pwn import *
print repr(p32(0x21DD09EC - u32('\x01\x01\x01\x01')*4))
