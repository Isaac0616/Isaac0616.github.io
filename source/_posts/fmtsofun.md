---
title: 'TW.edu CTF 2015: fmtsofun (pwn 150)'
date: 2016-02-18 13:23:45
categories:
- writeup
tags:
- format string
- pwn
- TW.edu CTF
---


## Description

> {% asset_link bofsofun binary %}
> Do you know format string attack ? 
> nc pwning.pwnable.tw 56026
> {% asset_link fmtsofun binary %}
> **Hint:**
> %n is so powerful

## Exploit

{% codeblock fmtsofun lang:x86asm line_number:false %}
.text:0x80486C7  mov    dword ptr [esp], offset format ; "Enter your format string :"
.text:0x80486CE  call   _printf
.text:0x80486D3  lea    eax, [esp+1Ch]
.text:0x80486D7  mov    [esp+4], eax
.text:0x80486DB  mov    dword ptr [esp], offset a79s ; "%79s"
.text:0x80486E2  call   ___isoc99_scanf
.text:0x80486E7  lea    eax, [esp+1Ch]
.text:0x80486EB  mov    [esp], eax      ; format
.text:0x80486EE  call   _printf
.text:0x80486F3  mov    dword ptr [esp], offset aHappyNewYear ; "\nHappy New Year !!"
.text:0x80486FA  call   _puts
{% endcodeblock %}

As the program's message suggests, the main purpose of this program is to let us launch a format string attack. I first use `fmtsofun_scout.py` to calibrate the argument number and padding of the input buffer.

{% include_code lang:python fmtsofun_scout.py %}

{% codeblock lang:bash line_number:false %}
$ python fmtsofun_scout.py 
Format string attack is so fun
Enter your format string :
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab10xfff7f3bc0x336141320x702439250x362570240xfff7f4b40xf7727000(nil)0x80484f00xf775f130
Happy New Year !!

argnum:7, padding:0
{% endcodeblock %}

With these information, we can now successfully perform the format string attack. However, this program only allow us to launch the attack once, which is not enough for us to both leak the address of stack and jump to the shellcode. To deal with this situation, I use GOT hijacking to make `puts` library call jumps to the address right brfore the bug. (Actually, I jump back to the point which is going to print the message "Enter your format string :" because it is easier to check wether the jump is success) Now we can lanuch the format string attack multiple times.

When I hijack the GOT entry of `puts` above, I also use `%33$x` to leak the 33rd argument on the stack, whose value seems to have a fix offset to the address of input buffer (I call it stack debris in my exploit) that allows us to calculate the address of the shellcode. After calculating the shellcode address, I use the same format string attack to hijack GOT entry of `puts` and jump to the shellcode.

{% include_code lang:python fmtsofun_exp.py %}

> Flag: `CTF{F0Rm4t_s7r!n6_!s_4wes0m3}`
