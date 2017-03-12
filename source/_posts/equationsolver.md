---
title: 'Internetwache CTF 2016: EquationSolver (exp 60)'
tags:
  - pwn
  - integer overflow
  - Internetwache CTF
categories:
  - writeup
date: 2016-03-04 15:58:39
---


## Description

> I created a program for an unsolveable equation system. My friend somehow forced it to solve the equations. Can you tell me how he did it?

## Exploit

This challenge asks us to solve the following equations.

{% codeblock lang:plain line_number:false %}
Solve the following equations:
X > 1337
X * 7 + 4 = 1337
{% endcodeblock %}

Obviously, the solution exists only if the integer overflow exists. I use Z3 to solve this problem.

{% include_code lang:python solve.py %}

{% codeblock lang:bash line_number:false %}
$ python solve.py
[x = 613566947]
{% endcodeblock %}

> Flag: `IW{Y4Y_0verfl0w}`
