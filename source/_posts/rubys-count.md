---
title: "Internetwache CTF 2016: Ruby's count (exp 50)"
tags:
  - pwn
  - regex
  - Internetwache CTF
categories:
  - writeup
date: 2016-03-04 10:22:26
---

## Description

> Hi, my name is Ruby. I like converting characters into ascii values and then calculating the sum.

## Exploit

{% codeblock lang:plain line_number:false %}
Let me count the ascii values of 10 characters:
abcdefghij
WRONG!!!! Only 10 characters matching /^[a-f]{10}$/ !
{% endcodeblock %}

So, now we know the matching regular expression. However, we can't achieve the target score by input only 10 [a-f] characters.

{% codeblock lang:plain line_number:false %}
Let me count the ascii values of 10 characters:
ffffffffff
Sum is: 1020
That's not enough (1020 < 1020)
{% endcodeblock %}

To input more characters, I make use of the feature of Ruby's regular expression describe in [this post](http://homakov.blogspot.tw/2012/05/saferweb-injects-in-various-ruby.html).

> ^ for start-of-string and $ for end-of-string ARE just new lines - \n!

Using following pattern, we can make the sum more than 1020 and get the flag.

{% include_code lang:python exp.py %}

> Flag: `IW{RUBY_R3G3X_F41L}`
