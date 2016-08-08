enc = 'IVyN5U3X)ZUMYCs'
print ''.join([chr(ord(c)^i) for i, c in enumerate(enc)])
