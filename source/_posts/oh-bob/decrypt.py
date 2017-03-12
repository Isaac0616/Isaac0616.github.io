from base64 import b64decode
import rsa

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m

n = 359567260516027240236814314071842368703501656647819140843316303878351
p = 17963604736595708916714953362445519
q = 20016431322579245244930631426505729
e = 65537
d = modinv(e, (p-1)*(q-1))
pk = rsa.PrivateKey(n, e, d, p, q)
print rsa.decrypt(b64decode('DK9dt2MTybMqRz/N2RUMq2qauvqFIOnQ89mLjXY='), pk)

n = 273308045849724059815624389388987562744527435578575831038939266472921
p = 16549930833331357120312254608496323
q = 16514150337068782027309734859141427
e = 65537
d = modinv(e, (p-1)*(q-1))
pk = rsa.PrivateKey(n, e, d, p, q)
print rsa.decrypt(b64decode('CiLSeTUCCKkyNf8NVnifGKKS2FJ7VnWKnEdygXY='), pk)

n = 333146335555060589623326457744716213139646991731493272747695074955549
p = 19193025210159847056853811703017693
q = 17357677172158834256725194757225793
e = 65537
d = modinv(e, (p-1)*(q-1))
pk = rsa.PrivateKey(n, e, d, p, q)
print rsa.decrypt(b64decode('AK/WPYsK5ECFsupuW98bCFKYUApgrQ6LTcm3KxY='), pk)
