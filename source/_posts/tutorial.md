---
title: 'CSAW CTF 2016: Tutorial (pwn 200)'
tags:
  - x86-64
  - pwn
  - CSAW CTF
  - ROP
categories:
  - writeup
date: 2016-09-29 01:01:39
---


## Description

> Ok sport, now that you have had your Warmup, maybe you want to checkout the Tutorial.
> nc pwn.chal.csaw.io 8002
> {% asset_link tutorial tutorial %} {% asset_link libc-2.19.so libc-2.19.so %}

## TL;DR
- A socket server
- Obvious leak of libc address and stack canary + provided libc library + stack buffer overflow
- ROP attack (`dup2`, `dup2`, `system("/bin/sh")`)

## Exploit

The direct execution of `tutorial` will crash. So, I inspect the binary with IDA Pro and found that this is a TCP server which requires a port number as the argument and a user call `tutorial` exists in the system. After slightly patching the program and providing the port number, I can run the program on my computer. Connecting to the server, it displays three options.

{% codeblock lang:plain line_number:false %}
-Tutorial-
1.Manual
2.Practice
3.Quit
>
{% endcodeblock %}

The first option `1.Manual` prints an address `Reference:0x7fad235d3860`, which is the address of `puts - 1280`. Together with the provided `libc-2.19.so`, it allows us to caculate the address of other functions in the libc.

The second option `2.Practice` asks us to input our exploit. Sending some random input, it seems to echo our input with some extra binary data in the end.

{% codeblock lang:plain line_number:false %}
>2
Time to test your exploit...
>abc
abc
��g�]�p�g/�-
{% endcodeblock %}

It turns out that these binary data are stack canary and part of the `rbp`. With the knowledge of stack canary and the address of functions in libc, now we can make use of the stack buffer overflow vulnerability of option 2 to conduct the ROP attack.

Notice that the server interacts with us via socket instead of standard input output. We can't merely invoke the `system("/bin/sh")`, which opens a shell only on the server side. The most common solution is using `dup2` to duplicate the file descriptor of socket connection to standard input and output before calling `system`. There are three ways to find out the file descriptor of the connection:
1. Educated guess. Functions usually return the lowest possible file descriptor. Standard input, output, and error are 0, 1, and 2 respectively. `socket` may return 3. Then `accept` is likely to return 4.
2. Leak stack buffer. Since we can leak the lower four bytes of `rbp`, we can easily guess the address of stack and leak the file descriptor stored in it.
3. `ls -l /proc/<pid>/fd`. Execute the program locally and inspect what file descriptors are being used.

The script is as follows.
{% include_code lang:python tutorial_exp.py %}

> Flag: `FLAG{3ASY_R0P_R0P_P0P_P0P_YUM_YUM_CHUM_CHUM}`

## Note
- **What I've learned:**
    - Using `dup2` to get the interactive shell of socket server.
    - There is no need to inject the string `/bin/sh` to somewhere in the buffer as I first did. This string is containing in the libc, and its offset can be found by `strings -t x libc-2.19.so | grep "/bin/sh"`
- This server using `fork` to create a new process to handle the new user's request, so the base address of `libc` and the value of stack canary remain the same from request to request. There is no need to automatically parse these value during the contest. Just hard code them in the script to save some time.
