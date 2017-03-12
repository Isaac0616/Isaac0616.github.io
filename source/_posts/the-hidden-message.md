---
title: 'Internetwache CTF 2016: The hidden message (misc 50)'
tags:
  - misc
  - Internetwache CTF
categories:
  - writeup
date: 2016-02-23 13:37:54
---

## Description

> My friend really can't remember passwords. So he uses some kind of obfuscation. Can you restore the plaintext?
> **Attachment:** {% asset_link misc50.zip %}

## Exploit

{% codeblock README.txt lang:plain line_number:false %}
0000000 126 062 126 163 142 103 102 153 142 062 065 154 111 121 157 113
0000020 122 155 170 150 132 172 157 147 123 126 144 067 124 152 102 146
0000040 115 107 065 154 130 062 116 150 142 154 071 172 144 104 102 167
0000060 130 063 153 167 144 130 060 113 012
0000071
{% endcodeblock %}

The file looks like the output of hexdump that every number represent a byte, and since these numbers exceed the ASCII range and the lack of 8 and 9, I suspect it is in octal. After transforming them from octal to ASCII I get:
`V2VsbCBkb25lIQoKRmxhZzogSVd7TjBfMG5lX2Nhbl9zdDBwX3kwdX0K\n`
Because all bytes are valid alphabet or number with the ending `\n`, this transform looks promising. Try to decode by base64 and I get:
`Well done!\n\nFlag: IW{N0_0ne_can_st0p_y0u}\n`

{% include_code lang:python decode.py %}

> Flag: `IW{N0_0ne_can_st0p_y0u}`

## Note

From other people's writeups, the offest which increases 20 for every 16 bytes also suggest that this file is in octal.
