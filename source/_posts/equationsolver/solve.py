from z3 import Solver, BitVec

s = Solver()
x = BitVec('x', 32)

s.add(x > 1337)
s.add(x*7 + 4 == 1337)

s.check()
print s.model()
