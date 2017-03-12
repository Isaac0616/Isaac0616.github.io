---
title: 'CSAW CTF 2016: Warmup (pwn 50)'
tags:
  - x86-64
  - pwn
  - CSAW CTF
categories:
  - writeup
date: 2016-09-20 11:49:23
---


## Description
> So you want to be a pwn-er huh? Well let's throw you an easy one ;)
> nc pwn.chal.csaw.io 8000
> {% asset_link warmup warmup %}

## Exploit

As the description said, this is a very straightforward question. Even without reversing the binary, it prints the address of the target function `system("cat flag.txt");` for us. Just buffer overflow the return address and jump to that funtion to get the flag.

{% codeblock lang:plain line_number:false %}
-Warm Up-
WOW:0x40060d
>
{% endcodeblock %}

{% include_code lang:python warmup_exp.py %}

> Flag: `FLAG{LET_US_BEGIN_CSAW_2016}`
