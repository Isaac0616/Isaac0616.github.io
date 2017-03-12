---
title: 'Codegate prequals 2017: babypwn (pwn 50)'
tags:
  - Codegate prequals
  - pwn
categories:
  - writeup
date: 2017-02-14 14:56:04
---


## Description

> BabyPwn~~~
> {% asset_link babypwn http://ctf.codegate.org/z/babypwn %}
> nc 110.10.212.130 8888
> nc 110.10.212.130 8889

## TL;DR
- Leak the canary
- Use ROP to leak the address of `libc` functions
- Find the `libc` version by [libcdb.com](libcdb.com)
- Use ROP to `dup2 dup2 system`

## Exploit

`babypwn` is a TCP server. If we connect to it, it is basically a echo server.

{% codeblock lang:plain line_number:false %}
▒▒▒▒▒▒▒C▒O▒D▒E▒G▒A▒T▒E▒2▒0▒1▒7▒▒▒▒▒▒▒
▒▒▒▒▒▒▒B▒A▒B▒Y▒P▒W▒N▒!▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒G▒O▒O▒D▒L▒U▒C▒K▒~▒!▒▒▒▒▒▒▒▒▒▒▒
===============================
1. Echo
2. Reverse Echo
3. Exit
===============================
Select menu > 1
Input Your Message : 123
123

===============================
1. Echo
2. Reverse Echo
3. Exit
===============================
Select menu > 2
Input Your Message : 123

321
===============================
1. Echo
2. Reverse Echo
3. Exit
===============================
Select menu >
{% endcodeblock %}

The bug is a simple buffer overflow. At line 10 of the following code snippet, it reads 0x64 bytes to a buffer of 0x28 bytes.

{% codeblock lang:c %}
send_str("\n===============================\n");
send_str("1. Echo\n");
send_str("2. Reverse Echo\n");
send_str("3. Exit\n");
send_str("===============================\n");
v1 = get_num();
if ( v1 != 1 )
  break;
send_str("Input Your Message : ");
recv_str(&v2, 0x64u);  // BUG
send_str(&v2);
{% endcodeblock %}

Although the return address is protected by a canary, this program doesn't append a null byte when receiving data and later return all the data before a null byte. Therefore, we can concatenate our input with the canary and leak it in the response of server. With the knowledge of canary, it is trivial to override the return address and launch a ROP attack.

I want to make use of the `system` to spawn a shell, so my next step is to leak the address of the `libc`. Using ROP chain such as `send, padding, GOT of atoi`, I can leak the address of several `libc` functions. Finally, I need to know the `libc` version of the remote to calculate the correct offset of `system`. At first, I used [libc-database](https://github.com/niklasb/libc-database) but couldn't find the matched version. Then, I try [libcdb.com](libcdb.com) and luckily found the target `{% asset_link libc-2.19_16.so libc %}`. Now, I can use the standard `dup2 dup2 system` ROP chain to launch a shell and get the flag.

The whole exploit is as follows. (Note that since it is a fork server, the canary and the `libc` base won't change unless the server is relaunched. Therefore, I hardcoded the canary and `libc` functions in the script.)

{% include_code lang:python babypwn_exp.py %}

> Flag: `FLAG{Good_Job~!Y0u_@re_Very__G@@d!!!!!!^.^}`

## Note
- I spent some unnecessary work on finding the address of `system` because I didn't see that `system` was already in the GOT table. It was deliberately put in the code that no one actually reference it. It was even used to `system("echo 'not easy to see'")` to indicate this fact. 
