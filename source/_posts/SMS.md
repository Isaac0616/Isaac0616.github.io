---
title: 'DefCamp CTF Finals 2016: SMS (pwn 200)'
tags:
  - pwn
  - DefCamp CTF
categories:
  - writeup
date: 2016-12-05 00:44:04
---


## Description
> nc 45.32.157.65 65022
> {% asset_link 200.bin 200.bin %}

## TL;DR
- Overflow the length variable.
- Overflow the return address to the built-in get shell function (Only overflow least two bytes to bypass ASLR).

## Exploit

{% codeblock lang:plain line_number:false %}
--------------------------------------------
|   Welcome to Defcamp SMS service          |
--------------------------------------------
Enter your name
> AAA
Hi, AAA
SMS our leader
> AAA
SMS delivered
{% endcodeblock %}

The binary let us input our name and a message. The memory layout looks like:

{% codeblock lang:plain line_number:false %}
Stack:
| SMS content (140 bytes) | name (40 bytes) | SMS length (1 byte) |
{% endcodeblock %}

The vulnerability is that when reading a name of 40 bytes, the correct for loop should be:

{% codeblock lang:plain line_number:false %}
for(int i = 0; i < 40; i++)
    ...
{% endcodeblock %}

instead of 

{% codeblock lang:plain line_number:false %}
for(int i = 0; i <= 40; i++)
    ...
{% endcodeblock %}

which causes a one byte overflow, and let us further overflow the return address when reading the SMS content. The target of the return is a built-in get shell function `frontdoor`. However, this program is PIE enabled, so we don't know the exact address of `frontdoor`. We can overcome it by only overriding the least two bytes of the return address. Since the least 12 bits are fixed, we are only guessing 4 bits of the address.

The complete script is as follows.

{% include_code lang:python sms_exp.py %}

> Flag: `DCTF{35c60be438186d13fdd2c9db9d3e33b7}`
