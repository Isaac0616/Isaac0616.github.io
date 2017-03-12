---
title: "Internetwache CTF 2016: It's Prime Time! (code 60)"
tags:
  - code
  - Internetwache CTF
categories:
  - writeup
date: 2016-03-03 13:35:27
---

## Description

> We all know that prime numbers are quite important in cryptography. Can you help me to find some?

## Exploit

In this challenge, we have to find the next prime to a given number 100 times to get the flag. The questions are in the following format. 

{% codeblock lang:plain line_number:false %}
Level 1.: Find the next prime number after 8:
{% endcodeblock %}

There is a `nextprime` function in SymPy, so we can solve this problem easily.

{% include_code solve.py %}

> Flag: `IW{Pr1m3s_4r3_!mp0rt4nt}`
