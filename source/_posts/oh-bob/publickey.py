import rsa

with open('bob.pub', 'rb') as f:
    pub1 = f.read()

with open('bob2.pub', 'rb') as f:
    pub2 = f.read()

with open('bob3.pub', 'rb') as f:
    pub3 = f.read()

print rsa.PublicKey.load_pkcs1_openssl_pem(pub1)
print rsa.PublicKey.load_pkcs1_openssl_pem(pub2)
print rsa.PublicKey.load_pkcs1_openssl_pem(pub3)
