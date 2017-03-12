---
title: 'Internetwache CTF 2016: File Checker (rev 60)'
tags:
  - reverse
  - Internetwache CTF
  - x86-64
categories:
  - writeup
date: 2016-02-26 13:36:13
---


## Description

> My friend sent me this file. He told that if I manage to reverse it, I'll have access to all his devices. My misfortune that I don't know anything about reversing :/
> **Attachment:** {% asset_link rev60.zip %}

## Exploit

{% codeblock filechecker lang:c %}
stream = fopen(".password", "r");
if ( stream )
{
  v4 = 15;
  value = 0;
  for ( i = 0; i < v4; ++i )
  {
    chr = fgetc(stream);
    if ( feof(stream) )
    {
      value |= 0x1337u;
      break;
    }
    sub_40079C(i, &chr);
    value |= chr;
  }
  if ( value <= 0 )
  {
    fclose(stream);
    puts("Congrats!");
    result = 0LL;
  }
  else
  {
    puts("Error: Wrong characters");
    result = 1LL;
  }
}
{% endcodeblock %}

{% codeblock sub_40079C lang:c %}
v4 = 4846;
v5 = 4832;
v6 = 4796;
v7 = 4849;
v8 = 4846;
v9 = 4843;
v10 = 4850;
v11 = 4824;
v12 = 4852;
v13 = 4847;
v14 = 4818;
v15 = 4852;
v16 = 4844;
v17 = 4822;
v18 = 4794;
v2 = (*(&v4 + i) + *chr) % 4919;
result = (unsigned int)v2;
*chr = v2;
{% endcodeblock %}

After decompiled by IDA pro, what the program does is really clear. It reads a string of 15 characters from file `.password` and check whether the following condition is satisfied.

{% codeblock lang:c line_number:false %}
(str[0] + V[0])%4919 | ... | (str[14] + V[14])%4919 <= 0,
where V = [4846, 4832, 4796, 4849, 4846, 4843, 4850, 
                4824, 4852, 4847, 4818, 4852, 4844, 4822, 4794]
{% endcodeblock %}

To satisfied the condition, just make every `(str[i] + V[i]) = 4919`. By the way, during the competition, when I saw the numbers `48xx` and `4919`, I was able to guess that the flag is the difference between two numbers. I have written a script to compute the flag.

{% include_code lang:python decode.py %}

> Flag: `IW{FILE_CHeCKa}`

## Note

**Learned:** How GCC optimize division and modulo operation. [Reference](http://reverseengineering.stackexchange.com/questions/1397/how-can-i-reverse-optimized-integer-division-modulo-by-constant-operations). Maybe I will read [Hacker's Delight](http://www.hackersdelight.org/) someday.
