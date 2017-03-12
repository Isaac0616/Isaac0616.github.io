---
title: "TW.edu CTF 2015: magicbox (pwn 100)"
date: 2016-02-01 00:33:58
categories:
- writeup
tags:
- pwn
- ROP
- TW.edu CTF
---

## Description

> This is a magic box. 
> nc pwning.pwnable.tw 56746
> {% asset_link magicbox binary %}

## Exploit

{% codeblock lang:plain line_number:false %}
--------------------------------
 1. Put a item to the box
 2. List the box
 3. Remove a item from the box
 4. give up the box
--------------------------------
Your choice :
{% endcodeblock %}

This program let us put "items" (16 bytes arbitrary user input) to the "box" (buffer located on the stack). However, it neither confines the amount of items nor enables the canary. Therefore, we can override the return address and inject our ROP chain. Moreover, this program is statically linked, so we can easily collect enough ROP gadgets.

I use [ROPgadget](https://github.com/JonathanSalwan/ROPgadget) to find out the gadgets needed. Then, I craft a ROP chain which reads `/bin/sh` to the free buffer located at `.bss` section and use it as the argument of `sys_execve` to spawn a shell.

{% include_code lang:python magicbox_exp.py %}

> Flag: `CTF{Pu7_R0p_74dg3t_!n_7h3_B0x_!s_m47iC}`

## Notes
At first, I assigned `free_buf = 0xffffd000` because I assumed it is an unused memory of the stack. However, I got the following error:

{% codeblock lang:plain line_number:false %}
set_thread_area failed when setting up thread-local storage
{% endcodeblock %}

I think it is due to the ASLR, which makes the stack address different every time. The address `0xffffd000` is only valid in `gdb` and generally unallocated. The section `.bss` or `.got` may be a better choice of the free buffer.
