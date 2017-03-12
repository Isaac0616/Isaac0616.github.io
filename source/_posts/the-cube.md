---
title: 'Internetwache CTF 2016: The Cube (rev 90)'
date: 2016-02-22 13:11:45
categories:
  - writeup
tags:
  - reverse
  - Internetwache CTF
---

## Description

> I really like Rubik's Cubes, so I created a challenge for you. I put the flag on the white tiles and scrambled the cube. Once you solved the cube, you'll know my secret.
> **Attachment:** {% asset_link rev90.zip %}

## Exploit

{% codeblock README.txt lang:plain line_number:false %}
Scrambling:
F' D' U' L' U' F2 B2 D2 F' U D2 B' U' B2 R2 D2 B' R' U B2 L U R' U' L'


White side:
-------
|{|3| |
| |D|R|
| |W| |
-------

Orange side:
-------
| | | |
| | | |
| | | |
-------

Yellow side:
-------
|}| | |
|3| | |
| | | |
-------


Red side:
-------
|I| | |
| | | |
| | |C|
-------

Green side:
-------
| | | |
| | | |
| | | |
-------

Blue side:
-------
| | | |
| | | |
| | | |
-------
{% endcodeblock %}

From the scrambled cube above, we know that the flag must be the permutation of `{3DRW}3IC`. We also know that the format of the flag is `IW{...}`. Therefore, the original white side should look like:

{% codeblock lang:plain line_number:false %}
White side:
-------
|I|W|{|
| | | |
| | |}|
-------
{% endcodeblock %}

Furthermore, no matter how we scramble the cube, central pieces will stay at center, corner pieces will stay at corner, and edge pieces will stay on edge, so we can deduce that the original white side should look like:

{% codeblock lang:plain line_number:false %}
White side:
-------
|I|W|{|
| |D| |
|C| |}|
-------
{% endcodeblock %}

Now, there are only three possible flags: `IW{3D3CR}`, `IW{3DRC3}`, and `IW{RD3C3}`. Just submit them respectively and we can figure out the correct flag is `IW{3DRC3}`.

> Flag: `IW{3DRC3}`
