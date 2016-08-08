from pwnlib.tubes.remote import remote

r = remote('188.166.133.53', 12037)
r.send('aaaaaaaaaa\naaaaaaaaaa\n')
print r.recvall()
