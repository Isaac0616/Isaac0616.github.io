---
title: 'PlaidCTF 2017: bigpicture (pwn 200)'
tags:
  - pwn
  - ASLR
  - libc hook
categories:
  - writeup
date: 2017-04-28 22:44:52
---


## Description
> Size matters!
> Running at bigpicture.chal.pwning.xxx:420
> {% asset_link bigpicture_0b8eed37d9a4e5073456306e6eb0672c.tgz Download %}

## TL;DR
- Request a large buffer which will be allocated at somewhere after the libc pages.
- The offset between the buffer and the libc is fixed.
- Use negative indexes to leak the base address of the libc.
- Set `__free_hook` to `system`.
- Set the content of the buffer to `/bin/sh`.
- `free(buffer)` becomes `system("/bin/sh")`.

## Exploit

This challenge comes with a source code {% asset_link bigpicture.c bigpicture.c %}. What it does is, first, allocating a 2D array with the height and the width we choose. Then, we can set the content of any element of the array. If an element has already been set, it will print out its value. Finally, it will draw the 2D array on the exit.

The vulnerability is that the index of the element to be set can be negative.

{% codeblock lang:c %}
if(x >= width || y >= height) {
    puts("out of bounds!");
    return;
}
{% endcodeblock %}

Therefore, we can leak or set the content before the buffer, which is usually in the heap. Next, here comes the essential part of the challenge. If the buffer located in the heap, the only memory pages we can access belong to the main program. Because of the full RELRO protection of this binary, we cannot hijack the control flow through overriding a GOT entry. Even worst, we don't know the exact offset between the buffer and the main program. However, if we request a large enough buffer (about 128kb), it will be allocated by `mmap`. This buffer will be placed after the `libc.so.6`, and the offset between these two memory pages is fixed. So, we can leak the libc address and override the `__free_hook` to divert the control flow. Now we know why the description said "Size matters!"

My exploit script is as follows.

{% include_code lang:python bigpicture_exp.py %}

I leak an address in the GOT section of the libc to calculate the base address of the libc. Then, I override `__free_hook` to `system` and the content of the buffer to `/bin/sh`. Now freeing the buffer at the end of the program becomes `system("/bin/sh")`. By the way, the offsets between the buffer and the libc of the remote machine were calculated by leaking some memory content and comparing then with the local one.

> Flag: `PCTF{draw_me_like_one_of_your_pwn200s}`

## Note
- **What I've learned:**
I know that the offsets between shared libraries are fixed. Through this challenge, I further confirm that the offsets between `mmap`ed pages are also fixed.
- Some references of ASLR:
    - [Exploiting Linux and PaX ASLR's weaknesses on 32- and 64-bit systems](https://www.blackhat.com/docs/asia-16/materials/asia-16-Marco-Gisbert-Exploiting-Linux-And-PaX-ASLRS-Weaknesses-On-32-And-64-Bit-Systems-wp.pdf)
    - [On the Eﬀectiveness of Full-ASLR on 64-bit Linux](https://cybersecurity.upv.es/attacks/offset2lib/offset2lib-paper.pdf)
