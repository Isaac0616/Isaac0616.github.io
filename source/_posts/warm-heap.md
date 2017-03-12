---
title: 'D-CTF Quals 2016: Warm heap (Exploit 100)'
tags:
  - D-CTF Quals
  - pwn
  - x86-64
  - heap overflow
  - GOT
categories:
  - writeup
date: 2016-10-04 16:46:04
---

## Description

> 10.13.37.21:1337
> {% asset_link exp100.bin https://dctf.def.camp/quals-2016/exp100.bin %}

## Exploit

{% asset_img warm_heap_1.png %}

The binary `malloc` four chunks as the figure shown above. The first and the third chunks contain a pointer to the second and the fourth chunks respectively. Then, it will invoke two `fgets` to these two pointers. We can make use of the buffer overflow bug of the first `fgets` to change the destination of the second `fgets`. By changing the value of the GOT of `exit` to the embedded print-flag function, we can get the flag easily.

{% include_code lang:python warm_heap_exp.py %}

> Flag: `DCTF{b94c21ff7531cba35a498cb074918b3e}`
