---
title: "TW.edu CTF 2015: mini (pwn 50)"
date: 2016-01-22 12:44:34
categories:
- writeup
tags:
- pwn
- TW.edu CTF
---

## Description

> Useless {% asset_link mini minibin %}
> nc 10.second.ninja 9090

## Exploit

This is an extremely short program.

{% codeblock lang:x86asm line_number:false %}
0x8048080 6A 03            push    3
0x8048082 6A FF            push    0FFFFFFFFh
0x8048084 6A 00            push    0
0x8048086 E8 10 00 00 00   call    sub_804809B
0x804808B 00*12
0x804809B 59               pop     ecx
0x804809C 5B               pop     ebx
0x804809D 5A               pop     edx
0x804809E 58               pop     eax
0x804809F CD 80            int     80h
{% endcodeblock %}

At `0x0804909F`, it will invoke `sys_read` with following parameters.

|eax|ebx (unsigned int fd)|ecx (char __user *buf)|edx (size_t count)|
|:---:|:---:|:---:|:---:|
|`0x03`|`0x00`|`0x804808B`|`0xFFFFFFFF`|

This would let us enter arbitrary length of input to `0x0804808B`. After the system call, the program will continue to execute the instruction at `0x08040A1`. Since `0x0804808B - 0x08040A1 = 22`, the program will execute from the 23rd byte of the user input. This is where we should put our shellcode.

{% include_code lang:python mini_exp.py %}

> Flag: `CTF{5he11c0d3_1s_Soo0o0ooOo_51mp13}`
