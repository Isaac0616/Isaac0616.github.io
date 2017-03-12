---
title: 'Codegate prequals 2017: meow (pwn 365)'
tags:
  - Codegate prequals
  - pwn
  - reverse
categories:
  - writeup
date: 2017-02-20 23:35:57
---


## Description
> Meow~Meow~
> {% asset_link meow http://ctf.codegate.org/z/meow %}
> nc 110.10.212.139 50410

## TL;DR
- Observe how user's input is used to "decrypt" the hard coded data
- Guess that the "decrypted" data should start with `push rbp; mov rbp, rsp;` and end with `leave; ret;`
- Brute force md5 with the constraints found above
- Use the ROP gadgets that author deliberately provide to launch a shell

## Exploit

{% codeblock lang:c %}
*(_QWORD *)s2 = 0x618F652224A9469FLL;
*(_QWORD *)&s2[8] = 1493362804178947496LL;
MD5_Init(&v2);
MD5_Update(&v2, input, 10LL);
MD5_Final(&s1, &v2);
return strncmp(&s1, s2, 0x10uLL) != 0;
{% endcodeblock %}

At the very beginning of the binary, it asks us to input a 10 bytes string of which md5 is equal to `9f46a92422658f61a80ddee78e7db914`... I tried searching this md5 on some online database but got no answer. Since it is also impossible to brute force an 80 bits input, I was totally stuck at this stage.

{% asset_img no_way.gif %}

When I was going to give up, one of my teammates reminded me that the input is also being used in the latter part of the program. Maybe we could find other constraints to reduce the search space of the input. It turned out to be the right direction, so let's see what the remaining program does.

{% codeblock lang:c %}
sub_D1D((__int64)&v12, (__int64)&input, v15);
sub_D1D((__int64)&v5, (__int64)&input, v14);
sub_1467((void **)&qword_2020B8, v17, v15, &v12);
sub_1467((void **)&unk_2020C0, v16, v14, &v5);
sub_C45();
{% endcodeblock %}

Roughly speaking, there are two segments of data. They are both operated with some sort of "decryption" in `sub_D1D` with our input as the key and then copied to a mmaped memory with the execute permission in `sub_1467`. Finally, in `sub_C45`, we can choose option 3 to jump to the first segment of the decrypted data and execute them as instructions.

Now, we know that at least the first segment of data should be decrypted to legal x86 instructions. Let's see what `sub_D1D` actually does.

{% codeblock sub_D1D lang:c %}
  v14 = 0;
  j = 0;
  v19 = 4;
  v18 = 5;
  v17 = 3;
  v13 = 10;
  v12 = 5;
  v11 = 7;
  v16 = 0;
  v15 = a3;
  v9 = 0LL;
  v10 = 0;
  v7 = 0;
  v8 = 0;
  v4 = 0;
  v5 = 0;
  v6 = 0;
  for ( i = 0; a3 - a3 % v11 > i; i += v11 )
  {
    for ( j = 0; j < v17; ++j )
      *((_BYTE *)&v4 + j) = *(_BYTE *)(j + v16 + initial_content);
    for ( j = 0; v11 - v17 > j; ++j )
      *((_BYTE *)&v4 + j + v17) = *(_BYTE *)(v17 + v15 - v11 + j + initial_content);
    for ( j = 0; j < v11; ++j )
      *((_BYTE *)&v4 + j) ^= *(_BYTE *)(j + user_input);  // user input
    for ( j = 0; j < v17; ++j )
      *(_BYTE *)(initial_content + j + v16) = *((_BYTE *)&v4 + j + v11 - v17);
    for ( j = 0; v11 - v17 > j; ++j )
      *(_BYTE *)(initial_content + v17 + v15 - v11 + j) = *((_BYTE *)&v4 + j);
    v16 += v17;
    v15 -= v11 - v17;
    v17 += 2;
    if ( v17 == 9 )
      v17 = 3;
  }
  v16 = 0;
  v15 = a3;
  for ( i = 0; a3 - a3 % v12 > i; i += v12 )
  {
    for ( j = 0; j < v18; ++j )
      *((_BYTE *)&v7 + j) = *(_BYTE *)(j + v16 + initial_content);
    for ( j = 0; v12 - v18 > j; ++j )
      *((_BYTE *)&v7 + j + v18) = *(_BYTE *)(v18 + v15 - v12 + j + initial_content);
    for ( j = 0; j < v12; ++j )
      *((_BYTE *)&v7 + j) ^= *(_BYTE *)(2 * j + 1LL + user_input);  // user input
    for ( j = 0; j < v18; ++j )
      *(_BYTE *)(initial_content + j + v16) = *((_BYTE *)&v7 + j + v12 - v18);
    for ( j = 0; v12 - v18 > j; ++j )
      *(_BYTE *)(initial_content + v18 + v15 - v12 + j) = *((_BYTE *)&v7 + j);
    v16 += v18;
    v15 -= v12 - v18--;
    if ( !v18 )
      v18 = 5;
  }
  v16 = 0;
  v15 = a3;
  for ( i = 0; a3 - a3 % v13 > i; i += v13 )
  {
    for ( j = 0; j < v19; ++j )
      *((_BYTE *)&v9 + j) = *(_BYTE *)(j + v16 + initial_content);
    for ( j = 0; v13 - v19 > j; ++j )
      *((_BYTE *)&v9 + j + v19) = *(_BYTE *)(v19 + v15 - v13 + j + initial_content);
    for ( j = 0; j < v13; ++j )
      *((_BYTE *)&v9 + j) ^= *(_BYTE *)(j + user_input);  // user input
    for ( j = 0; j < v19; ++j )
      *(_BYTE *)(initial_content + j + v16) = *((_BYTE *)&v9 + j + v13 - v19);
    for ( j = 0; v13 - v19 > j; ++j )
      *(_BYTE *)(initial_content + v19 + v15 - v13 + j) = *((_BYTE *)&v9 + j);
    v16 += v19;
    v15 -= v13 - v19++;
    if ( v19 == 9 )
      v19 = 4;
  }
  v16 = 0;
  v15 = a3;
  v19 = 4;
  for ( i = 0; a3 - a3 % v13 > i; i += v13 )
  {
    for ( j = 0; j < v19; ++j )
      *((_BYTE *)&v9 + j) = *(_BYTE *)(j + v16 + initial_content);
    for ( j = 0; v13 - v19 > j; ++j )
      *((_BYTE *)&v9 + j + v19) = *(_BYTE *)(v19 + v15 - v13 + j + initial_content);
    for ( j = 0; j < v13; ++j )
      *((_BYTE *)&v9 + j) ^= *(_BYTE *)(j + user_input);  // user input
    for ( j = 0; j < v19; ++j )
      *(_BYTE *)(initial_content + j + v16) = *((_BYTE *)&v9 + j + v13 - v19);
    for ( j = 0; v13 - v19 > j; ++j )
      *(_BYTE *)(initial_content + v19 + v15 - v13 + j) = *((_BYTE *)&v9 + j);
    v16 += v19;
    v15 -= v13 - v19++;
    if ( v19 == 9 )
      v19 = 4;
  }
{% endcodeblock %}

The decompiled code is quite complicated, but we can see that the user's input is only involved in some xor operations. Maybe we can find out what this code snippet does by observing the input and the output of it. To do this, I first patched the md5 checking and input `'\x00'*10` to see what is the effect without user's input through `gdb`.

{% codeblock lang:plain line_number:false %}
input:
f1 64 72 4a 4f 48 4d ba 77 73 1d 34 f5 af b8 0f
24 56 11 65 47 a3 2f 73 a4 56 4f 70 4a 13 57 9c
3f 6f 06 61 40 90 af 39 10 29 34 c3 00 7a 40 3d
4e 3f 0e 2a 2f 20 7f 73 89 7d 4b 1d 09 aa d0 00
21 89 4d 2a 67 7c 18 3b 39 f2 8d 1c a7 71 57 2e
31 14 67 48 3c 7d af 70 ae 10 31 68 d1 26 05 c8
25 f2 62 f5 5d 38 34 f2 20 0e 7e 9f fb 57 72 26
57 67 15 10 15 13 b9 3e 79 89 5d 24 12 01 98 7b
18 25 e0 df 7c 24 1b 2d 44 b0 10 3d 57 3d 62 b4
21 1d 3e d1 10 d7 45 74 96 2b 6d 3b ed 10 00 67
31 df 6c b8 86 1a 7c 6b 64 78 c6 37 76 e6 61 a0
ad be 4c ba a7 0d

output:
0d 48 f5 af 4d ad be 77 4c a4 56 34 64 72 4f 37
31 6f 70 e6 61 a0 11 9c 3f 06 13 3d 73 65 78 61
34 c3 40 86 1a af 40 7f 73 29 3f 7a 6d 67 68 d1
7d df 6c b8 71 2e 1c 62 1d 31 20 10 10 89 39 f2
4d 96 2b 67 05 3c 7d 3b 44 26 7e d1 01 98 70 d7
45 74 79 25 24 7b 10 24 48 89 1d c8 34 f2 25 57
3d 62 7c 26 57 38 3e df 13 b0 10 b9 10 3d 72 1b
20 2d 67 15 15 f5 5d f2 b4 21 af 12 31 14 3e 9f
57 ae 18 67 8d 5d e0 fb 0e 7c 18 2a 3b ed 89 a7
0e 2a 00 4e aa 4b 57 2f 00 00 21 09 d0 39 10 90
6b 64 4f 7c 47 a3 c6 f1 76 4a 57 2f b8 0f 24 56
4a 73 1d ba ba a7
{% endcodeblock %}

If we observe the input and the output carefully, we would find that the code is only shuffling the input. Then, it is time to exam the effect of the user's input. Using the same procedure, we can easily find that every byte of user's input is xor with some fixed bytes of data, so I wrote a script to visualize this operation.

{% include_code lang:python find_pattern.py %}

The output would looks like (only portion):

{% asset_img pattern.png %}

Data affected by the nth byte of user's input are highlighted. Now, we know how the "decryption" works. If we also know what the decrypted code should be, we can derive the input inversely. Unfortunately, we have no clue about the decrypted code. However, it is reasonable to guess that the prologue and epilogue should be the standard `push rbp; mov rbp, rsp;` and `leave; ret;`. With only these bytes of information, we can establish several relations between bytes of user's input and shrink the search space of md5 to a small range. (By the way, these relations suggest that the MSB of the xor of any two bytes of user's input is `0`, so I boldly guess that the input is printable.)

I wrote a C code to brute force the correct user's input, which is `$W337k!++y`.

{% include_code lang:c bruteforce.c %}

After providing the correct input, the challenge is still not finished.

{% codeblock lang:plain line_number:false %}
***** hello? *****
>>> $W337k!++y
- What kind of pet would you like to have?
- Select the number of pet!
1. angelfish
2. bear
3. cat
4. dog
5. I don't want pets
# number = 3
Did you choose a cat?????
What type of cat would you prefer? '0'
>>>
{% endcodeblock %}

The decrypted code is:

{% codeblock lang:x86asm First part of decrypted code %}
push   rbp
mov    rbp,rsp
sub    rsp,0x60
movabs rax,0x20756f7920646944

mov    QWORD PTR [rbp-0x60],rax
movabs rax,0x612065736f6f6863

mov    QWORD PTR [rbp-0x58],rax
movabs rax,0x3f3f3f3f74616320

mov    QWORD PTR [rbp-0x50],rax
movabs rax,0x7420746168570a3f

mov    QWORD PTR [rbp-0x48],rax
movabs rax,0x6320666f20657079

mov    QWORD PTR [rbp-0x40],rax
movabs rax,0x646c756f77207461

mov    QWORD PTR [rbp-0x38],rax
movabs rax,0x65727020756f7920

mov    QWORD PTR [rbp-0x30],rax
movabs rax,0x273027203f726566

mov    QWORD PTR [rbp-0x28],rax
mov    DWORD PTR [rbp-0x20],0x3e3e3e0a
mov    BYTE PTR [rbp-0x1c],0x0
lea    rax,[rbp-0x60]
mov    edx,0x44
mov    rsi,rax
mov    edi,0x1
mov    eax,0x1
syscall
lea    rax,[rbp+0x8]
mov    edx,0x18
mov    rsi,rax
mov    edi,0x0
mov    eax,0x0
syscall
nop
leave
ret
{% endcodeblock %}

It reads `0x18` bytes to the return address just before returning, which means we have a three-gadget ROP. Since this is a PIE binary, and we don't have any information leak, and the ROP chain is extremely short, it seems that we can basically do nothing. Nevertheless, the author of the program has deliberately put the exact three gadgets that we need in the second part of the data. Because the second part of the data is located in a mmaped memory of which address is known, we can easily use them to launch the shell.

{% codeblock lang:x86asm Second part of decrypted code%}
push   rbp
mov    rbp, rsp
sub    rsp, 0x10
mov    qword ptr [rbp - 8], rdi
mov    rax, qword ptr [rbp - 8]
mov    edx, 0
mov    esi, 0
mov    rdi, rax
mov    eax, 0x3b
syscall
nop
leave
ret
.byte 0x00
.byte 0x00
.ascii '/bin/sh'
.byte 0x00
.byte 0x00
.byte 0x00
.byte 0x00
.byte 0x00
.byte 0x00
pop    rdi
ret
{% endcodeblock %}

The exploit script is as follows.

{% include_code lang:python meow_exp.py %}

> Flag: `flag{what a lovely kitty!}`
