---
title: 'HITCON CTF 2016: Secret Holder (pwn 100)'
tags:
  - pwn
  - HITCON CTF
  - heap
  - unsafe unlink
  - use after free
  - GOT
categories:
  - writeup
date: 2016-10-29 20:46:05
---


## Description

> Break the Secret Holder and find the secret.
> nc 52.68.31.117 5566
> {% asset_link SecretHolder_d6c0bed6d695edc12a9e7733bedde182554442f8 SecretHolder %}

## TL;DR
- Free the chunk of others to create use after free.
- Overlapping three chunks to overwrite chunk headers.
- Unsafe unlink.
- Change `free` GOT entry to `puts` PLT address to leak `libc` base.
- Change `atoi` GOT entry to `system` in `libc` to get the shell.

## Exploit

{% codeblock lang:plain line_number:false %}
Hey! Do you have any secret?
I can help you to hold your secrets, and no one will be able to see it :)
1. Keep secret
2. Wipe secret
3. Renew secret
1
Which level of secret do you want to keep?
1. Small secret
2. Big secret
3. Huge secret
{% endcodeblock %}

The program allows us to conduct three kinds of operations on three different sizes of secrets.

Three operations:
1. Keep secret: `calloc` corresponding size of memory and read some input to it.
2. Wipe secret: `free` the corresponding memory.
3. Renew secret: Overwrite the content of the corresponding memory.

Three secrets:
1. Small secret: 40 bytes
2. Big secret: 4000 bytes
3. Huge secret: 400000 bytes

We can only keep at most one secret per size. Three pointers of the secret are store on the `.bss` section with three flags which indicate whether the secret has been allocated.

The vulnerability comes from the `wipe` function. The program will check whether the secret has been created in `keep` and `renew` but not in `wipe`, so we can `free` an already freed secret. `free` a secret twice consecutively would only make the program crash due to the double free detection. However, if we keep another secret on the same address after the first `free`, we can `free` this new secret through the old pointer. Then, since the new secret doesn't aware of this `free`, we can still write data to it and cause an use after free vulnerability.

For example, if we invoke functions in the following sequence:
`keep('small') -> wipe('small') -> keep('big') -> wipe('small') -> keep('small')`

The heap layout would be like:
{% asset_img heap1.png %}

We can now overflow the header of the top chunk. There is a technique call "House of force", which is related to modify the header of the top chunk. However, it also requires the ability to `malloc` arbitrary size, so this program is not the case.

I was stuck in here for a while until I accidentally found an interesting fact of heap. The huge secret is too large to fit in the main arena, so it supposed to be allocated by `mmap`. It does call `mmap` at the first time, however, if I `free` the memory and `malloc` again, the new memory chunk will surprisingly appear in the main arena. I can't find the description of this property on related heap exploit document. Maybe I should check it out in the source code someday. Anyway, this property turns out to be the key point of solving this problem.

We first invoke functions as the previous example with additional `keep(huge) -> wipe(huge) -> keep(huge)`. The heap layout would become:
{% asset_img heap2.png %}

Then, we are able to modify the content of the small secret and the header of the huge secret. These abilities plus the pointer of the secrets on `.bss` section enable a classical attack call "unsafe unlink". I create a fake freed chunk in the small secret, whose `fd` and `bk` points to `small secret pointer - 0x18` and `small secret pointer - 0x10` respectively, and change the PREV_INUSE bit of the huge secret to 0. After wiping the modified huge secret, the small secret pointer would point to a little offset before itself, allowing us to overflow three secret pointers and further get the arbitrary write.

Before modifying GOT entry to `system`, we have to leak the base of `libc` first. I achieve it by changing the `free` GOT entry to the address of `puts` in `.plt` section and make the big secret pointer point to `read` GOT entry. Then, calling wipe on the big secret would print the address of `read` and leak the address of `libc` (I guessed the `libc` binary is the same as another pwn problem. {% asset_link libc.so.6_375198810bb39e6593a968fcbcf6556789026743 libc.so %}).

Finally, we can change the `atoi` GOT entry to `system`, and input `"sh"` to get the shell. The whole exploit is as follows.

{% include_code lang:python secret_holder_exp.py %}

> Flag: `hitcon{The73 1s a s3C7e+ In malloc.c, h4ve y0u f0Und It?:P}`

## Note
**What I've learned:**
The behavior of `malloc` when the requested size is greater than the main arena limit.
