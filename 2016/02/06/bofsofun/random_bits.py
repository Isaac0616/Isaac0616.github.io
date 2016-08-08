gdb.execute('b *main+58', to_string=True)
gdb.execute('set disable-randomization off')

address = []
for i in range(20):
    gdb.execute('r > /dev/null', to_string = True)
    # Read the value of eax, which contains the address of input buffer
    b = bin(int(str(gdb.parse_and_eval('$eax')), 16))
    address.append(b[2:])
    print b

# Find out the highest and lowest bits that vary every time
high = -1
for i, n_bit in enumerate(zip(*address)):
    if len(set(n_bit)) > 1:
        if high == -1:
            high = i
        low = i

print "Random range: [{}, {}], {} bits".format(high, low, low - high + 1)
