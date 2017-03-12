---
title: 'Internetwache CTF 2016: A numbers game (code 50)'
tags:
  - code
  - Internetwache CTF
categories:
  - writeup
date: 2016-03-03 09:35:14
---

## Description

> People either love or hate math. Do you love it? Prove it! You just need to solve a bunch of equations without a mistake.

## Exploit

In this challenge, we need to solve 100 equations to get the flag. The equations are in the following form.

{% codeblock lang:plain line_number:false %}
Level 1.: x * 14 = 238

Level 2.: x + 35 = 43
{% endcodeblock %}

There is no special technique. Just parse the equations and solve it.

{% include_code solve.py %}

> Flag: `IW{M4TH_1S_34SY}`
