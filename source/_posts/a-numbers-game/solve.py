from pwnlib.tubes.remote import remote

r = remote('188.166.133.53', 11027)

while True:
    lines = r.recvlines(2)
    print '\n'.join(lines)
    sp = lines[1].split()

    # sp[3] is the operator
    # sp[4] is the operand on the left side
    # sp[6] is the operand on the right side
    if sp[3] == '+':
        x = int(sp[6]) - int(sp[4])
    elif sp[3] == '-':
        x = int(sp[6]) + int(sp[4])
    elif sp[3] == '*':
        x = int(sp[6]) / int(sp[4])
    elif sp[3] == '/':
        x = int(sp[6]) * int(sp[4])

    print x
    r.sendline(str(x))
