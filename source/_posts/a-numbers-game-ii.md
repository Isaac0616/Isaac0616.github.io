---
title: 'Internetwache CTF 2016: A numbers game II (code 70)'
tags:
  - code
  - Internetwache CTF
categories:
  - writeup
date: 2016-03-03 22:23:14
---

## Description

> Math is used in cryptography, but someone got this wrong. Can you still solve the equations? 
> **Hint:** You need to encode your answers.
> **Attachment:** {% asset_link code70.zip %}

## Exploit

This challenge is different from {% post_link a-numbers-game "A numbers game (code 50)" %} with only an additional encode/decode process. The encode function has been provided.

{% codeblock lang:python %}
def encode(self, eq):
    out = []
    for c in eq:
        q = bin(self._xor(ord(c),(2<<4))).lstrip("0b")
        q = "0" * ((2<<2)-len(q)) + q
        out.append(q)
    b = ''.join(out)
    pr = []
    for x in range(0,len(b),2):
        c = chr(int(b[x:x+2],2)+51)
        pr.append(c)
    s = '.'.join(pr)
    return s
{% endcodeblock %}

The result of the encoded equations look like:

{% codeblock lang:plain line_number:false %}
Level 1.: 4.4.5.3.3.3.3.3.3.3.5.6.3.3.3.3.3.4.3.4.3.4.4.4.3.3.3.3.3.4.6.4.3.3.3.3.3.4.3.6.3.4.4.3
{% endcodeblock %}

What `encode` function does is 
1. Xor every charactors with 32 (e.g. 'x' -> 88)
2. Convert every charactors to the binary form with padding 0 (e.g. 88 -> '01011000')
3. Concatenate the result in 2.
4. Convert every two digits into integer and plus 51 (e.g. '01011000' -> [52, 52, 53, 51])
5. Convert the numbers above to charactors and concatenate them with '.' (e.g. [52, 52, 53, 51] -> '4.4.5.3')

To decode, just reverse the process above. With the encode and decode function, we can use the same program shown in {% post_link a-numbers-game "A numbers game (code 50)" %} to solve the program and get the flag.

{% include_code solve.py %}

> Flag: `IW{Crypt0_c0d3}`
