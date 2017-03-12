---
title: 'D-CTF Quals 2016: My gift (Exploit 200)'
tags:
  - D-CTF Quals
  - pwn
  - stack overflow
  - x86-64
categories:
  - writeup
date: 2016-10-04 19:08:36
---


## Description

> 10.13.37.22:1337
> {% asset_link exp200.bin https://dctf.def.camp/quals-2016/exp200.bin %}

## Exploit

This is a straightforward echo server with a bare buffer overflow vulnerability. Stack canary is not enable, and there is even a hidden print-flag function in the binary. So, just overflow the return address and jump to the target in the old-school fashion. To trigger the `ret`, we need to enter a string whose position 0, 1, 2, 4 are s, t, o, p respectively.

{% include_code lang:python my_gift_exp.py %}

> Flag: `DCTF{53827349d071f72d5cbcc37d3a14ca39}`
