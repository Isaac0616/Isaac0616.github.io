from base64 import b64decode
from PIL import Image
from zbarlight import scan_codes

def create_qrcode(qr):
    img = Image.new('1', (23, 23), 'white')
    qr = qr.split('\n')

    for i in range(1, 22):
        for j in range(2, 44, 2):
            if qr[i][j] == ' ':
                img.putpixel((i, j/2), 0) # add a black block

    return img


with open('README.txt') as f:
    lines = f.read().split('\n')[:-1]

b64code = ''
message = ''
for l in lines:
    b64code += l
    if len(l) < 76:
        qr_text = b64decode(b64code).decode('utf8')
        qrcode = create_qrcode(qr_text)
        message += scan_codes('qrcode', qrcode)[0]
        b64code = ''

        #qrcode.resize((500, 500)).show()
        #raw_input('')

print message
