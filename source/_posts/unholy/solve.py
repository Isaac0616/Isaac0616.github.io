from numpy import array, dot, float64
from numpy.linalg import inv
from pwn import *

# reverse Part3: matrix multiplication
Y = array([[383212, 38297, 8201833],
           [382494, 348234985, 3492834886],
           [3842947, 984328, 38423942839]], float64)
n = array([[5034563854941868,252734795015555591,55088063485350767967],
           [-2770438152229037,142904135684288795,-33469734302639376803],
           [-3633507310795117,195138776204250759,-34639402662163370450]], float64)

#matrix = [-1304886577, 722035088, 1368334760,
#           1473172750, 412774077, -908901225,
#           -490967005, 563111828, -952589187, 1306786301]
matrix = dot(n, inv(Y)).round().astype(int).flatten().tolist() + [1306786301]

# reverse Part2
key = [1952540791, 1768908659, 1852794734, 1701995880]
v8 = 0;
ary11 = []
ary12 = []

# compute the needed constant
while True:
    v11 = v8 + key[v8 & 3];
    ary11.append(v11)
    v8 = (v8 - 1640531527)&0xffffffff;
    v12 = v8 + key[(v8 >> 11) & 3]
    ary12.append(v12)

    if v8 == -957401312&0xffffffff:
        break

flag = ''
for i in range(0, len(matrix), 2):
    v9 = matrix[i]&0xffffffff
    v10 = matrix[i+1]&0xffffffff

    for j in reversed(range(32)):
        v10 = (v10 - (ary12[j] ^ ((16*v9 ^ (v9 >> 5)) + v9)))&0xffffffff
        v9 = (v9 - (ary11[j] ^ ((16*v10 ^ (v10 >> 5)) + v10)))&0xffffffff

    flag += p32(v9) + p32(v10)

print flag[:-4]
