---
title: '0CTF 2017 Quals: EasiestPrintf (pwn 150)'
tags:
  - pwn
  - format string
  - libc hook
  - printf
categories:
  - writeup
date: 2017-03-23 02:12:03
---


## Description
> Warm UP! A traditional Format String Attack.
> It's running on Debian 8.
> nc 202.120.7.210 12321
> {% asset_link EasiestPrintf EasiestPrintf %}
> {% asset_link libc.so.6_0ed9bad239c74870ed2db31c735132ce libc.so.6 %}

## TL;DR
- Leak the libc address from the free arbitrary read.
- Use format string to modify `__free_hook` to the one-gadget and trigger it by a format placeholder with large width field.

## Exploit

This is a simple binary. After some setup, it first gives us an arbitrary read and then a 159-byte format string vulnerability. The problem is that this is a Full RELRO binary, so we can not change the GOT value to hijack the control flow. Moreover, because the `printf` is immediately followed by an `_exit`, we have to exploit in a single format string.

Several ideas come to my mind.
1. Because it is a 32-bit binary, maybe we can brute force the return address of `printf`.
2. Exploit the `exit` function, maybe something like `atexit` function pointer is exploitable.
3. Change the value of `__malloc_hook` or `__free_hook` and find a way to trigger them in `printf`.

For the first idea, the search space is large, and both the manual randomization of stack through `alloca` and `sleep(3)` at the beginning of the binary discourage this solution.

For the second idea, `atexit` function pointers are encrypted, and this binary use `_exit` instead of `exit`, which won't trigger `atexit` functions anyway.

Finally, the third idea works out. By searching `malloc` in `vfprintf.c`, it seems that we can trigger `malloc` and the following `free` if the width field of the format placeholder is large enough.

{% codeblock vfprintf.c lang:c %}
if (width >= WORK_BUFFER_SIZE - 32)
  {
    size_t needed = ((size_t) width + 32) * sizeof (CHAR_T);
    ...
    workstart = (CHAR_T *) malloc (needed);
{% endcodeblock %}

Although it took me quite a while to come up with the solution, the final exploitation is short and straightforward.

1. Leak the libc address from the arbitrary read.
2. Construct a format string with
  1. the `%hhn` trick to modify `__free_hook` to the one-gadget.
  2. `%100000c` to trigger `malloc` and `free`.

I choose `__free_hook` instead of `__malloc_hook` because the address of `__malloc_hook` contains a `\x0a` byte which will break the reading of the input.

The full script is as follows.
{% include_code lang:python EasiestPrintf_exp.py %}

> Flag: `flag{Dr4m471c_pr1N7f_45_y0u_Kn0w}`

## Note
- **What I've learned:**
  - Both `printf` and `scanf` can trigger `malloc` and `free`.
- There are couples of solutions for this challenge. See [this video](https://www.youtube.com/watch?v=kEqOvWmzu6Y) for more details.
