---
title: "TW.edu CTF 2015: bofsofun (pwn 150)"
date: 2016-02-06 20:31:28
categories:
- writeup
tags:
- ASLR
- pwn
- TW.edu CTF
---

## Description

> Do you know Stack overflow attack ? 
> nc pwning.pwnable.tw 48879
> {% asset_link bofsofun binary %}

## Exploit

{% codeblock bofsofun lang:x86asm line_number:false %}
.text:0x823    lea   eax, (aBufferOverflow - 1FB0h)[ebx] ; "Buffer overflow is so fun"
.text:0x829    mov   [esp], eax      ; s
.text:0x82C    call  _puts
.text:0x831    lea   eax, (aEnterYourMagic - 1FB0h)[ebx] ; "Enter your magic :"
.text:0x837    mov   [esp], eax      ; format
.text:0x83A    call  _printf
.text:0x83F    lea   eax, [esp+10h]
.text:0x843    mov   [esp+4], eax
.text:0x847    lea   eax, (aS - 1FB0h)[ebx] ; "%s"
.text:0x84D    mov   [esp], eax
.text:0x850    call  ___isoc99_scanf
.text:0x855    lea   eax, (aHappyNewYear - 1FB0h)[ebx] ; "\nHappy New Year !!"
.text:0x85B    mov   [esp], eax      ; s
.text:0x85E    call  _puts
{% endcodeblock %}

There is a straightforward buffer overflow bug of `scanf("%s")` at `0x850`, and as we can see from the output of `checksec` below, the `NX` and `STACK CANARY` is disabled. It seems that we can insert the shellcode and jump to it. However, also shown in the output of `checksec`, this is a **PIE enabled** program. That is, with only one time buffer overflow, we can't decide where the shellcode or any other portion of the program are located.

{% codeblock lang:bash line_number:false %}
$ checksec --file bofsofun
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FORTIFY FORTIFIED FORTIFY-able  FILE
Full RELRO      No canary found   NX disabled   PIE enabled     No RPATH   No RUNPATH   No      0               1       bofsofun
{% endcodeblock %}

To deal with this problem, I adopt the brute force attack which makes use of the low entropy of ASLR on 32-bit systems. I choose a possible address of shellcode and run the exploit repeatedly until it successfully return to the shellcode. This [wiki](https://en.wikipedia.org/wiki/Address_space_layout_randomization) page has the information needed for this exploit. According to it, Linux supplies only 19 bits of stack entropy on a period of 16 bytes. It is also verified by `random_bits.py`, the gdb script which runs the program 20 times to exam the randomness of the address of input buffer where I will put my shellcode.

{% include_code lang:python random_bits.py %}

{% codeblock lang:plain line_number:false %}
gdb-peda$ source random_bits.py 
0b11111111100110111111000101100000
0b11111111111001100011001110000000
0b11111111100101100111111101000000
0b11111111101010110010011110010000
0b11111111101000100000010000100000
0b11111111111101011101011010100000
0b11111111100101011001000000110000
0b11111111101001100101010000010000
0b11111111111110000110111101000000
0b11111111101111011111011111110000
0b11111111110010110010100110010000
0b11111111101000001110001111110000
0b11111111111010010000001110000000
0b11111111101100101010101011000000
0b11111111101100110100001100110000
0b11111111101000100110000010000000
0b11111111110100001000110011110000
0b11111111111010110000101110110000
0b11111111111111001101010011010000
0b11111111100110001001000011000000
Random range: [9, 27], 19 bits
{% endcodeblock %}

To further reduce the entropy, I also adopt a 2048-bit nop sled. Under this situation, the probability of jumping to the shellcode is theoretically $\frac{2^{11} \div 2^4}{2^{19}} = \frac{1}{4096} \approx 0.02\%$, which is also consistent to the result of real exploitation.

{% include_code lang:python bofsofun_exp.py %}

> Flag: `CTF{4Slr_!S_w34kn3Ss_0n_x86_3z}`

## Note

At first, I thought that the success rate is $\frac{2^{11}}{2^{19}} = \frac{1}{256} \approx 0.4\%$ because I didn't consider the fact that the lowest 4 bits are not included in the 19-bit randomness. In short, only every extra $2^4$ of nop sled could effectively increase $\frac{1}{2^{19}}$  of success rate. Therefore, we should divide the length of nop sled by $2^4$, and the final success rate is $\frac{2^{11} \div 2^4}{2^{19}} = \frac{1}{4096} \approx 0.02\%$ as shown above.
