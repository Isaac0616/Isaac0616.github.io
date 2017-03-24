---
title: '0CTF 2017 Quals: Baby Heap 2017 (pwn 255)'
tags:
  - pwn
  - heap
  - overlapping chunks
  - fastbin corruption
categories:
  - writeup
date: 2017-03-24 14:21:41
---


## Description
> Let's practice some basic {% asset_link babyheap_69a42acd160ab67a68047ca3f9c390b9 heap %} techniques in 2017 together!
> 202.120.7.218:2017
> {% asset_link libc.so.6_b86ec517ee44b2d6c03096e0518c72a1 libc.so.6 %}

## TL;DR
- Overlapping two chunks to leak the address of the libc.
- Use fastbin corruption to override the value of `__malloc_hook` to one-gadget.

## Exploit

{% codeblock lang:plain line_number:false %}
===== Baby Heap in 2017 =====
1. Allocate
2. Fill
3. Free
4. Dump
5. Exit
Command:
{% endcodeblock %}

This is a classical pwn challenge of heap with four kinds of operations: `malloc`, `free`, read, write. The only difference is that it use `calloc`, which initialzes the memory to zero, instead of the usual `malloc`. The challenge further increases its difficulty in two ways. First, it enables PIE and put the array of the `malloc` pointers in a random `mmap` area. Therefore, we do not know the address to launch the "unsafe unlink" attack. Second, it also enables RELRO so that we cannot change the value of GOT table to hijack the control flow. In contrast, the vulnerability is evident. We can fill the arbitrary length of input to the heap and overflow anything after that.

To solve this challenge, I first leak the address of the libc by overlapping two chunks as follows (also a common attack).

{% asset_img baby_heap_2017.png %}

Then, I override the `fd` pointer of a freed fastbin chunk to somewhere before `__malloc_hook` which has a valid "chunk size." Finally, after two `malloc` of the proper size, I get a chunk which allows me to change the `__malloc_hook` to one-gadget.

Note that the checking of the chunk size of the fastbin in `malloc.c` is not strict. It only checks whether the size divided by 16 (64bit) equals to the same index. There is no requirement of alignment, and it views the size as a 4-byte integer. Therefore, in this challenge, I took `0x7f` as the chunk size of a `0x70` fastbin chunk.

{% codeblock malloc.c lang:c %}
#define fastbin_index(sz) \
  ((((unsigned int) (sz)) >> (SIZE_SZ == 8 ? 4 : 3)) - 2)
...
if (__builtin_expect (fastbin_index (chunksize (victim)) != idx, 0))
  {
    errstr = "malloc(): memory corruption (fast)";
{% endcodeblock %}

The full script is as follows.
{% include_code lang:python babyheap_exp.py %}

> Flag: `flag{you_are_now_a_qualified_heap_beginner_in_2017}`
