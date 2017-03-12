---
title: 'Internetwache CTF 2016: Eso Tape (rev 80)'
tags:
  - reverse
  - Internetwache CTF
  - esoteric
categories:
  - writeup
date: 2016-02-29 14:50:05
---

## Description

> Description: I once took a nap on my keyboard. I dreamed of a brand new language, but I could not decipher it nor get its meaning. Can you help me? 
> **Hint:** Replace the spaces with either '{' or '}' in the solution. 
> **Hint:** Interpreters don't help. Operations write to the current index.
> **Attachment:** {% asset_link rev80.zip %}

## Exploit

{% codeblock priner.tb lang:plain line_number:false %}
## %% %++ %++ %++ %# *&* @** %# **&* ***-* ***-* %++ %++ @*** *-* @*** @** *+** @*** ***+* @*** **+** ***+* %++ @*** #% %% %++ %++ %++ %++ @* %# %++ %++ %++ %% *&** @* @*** *-** @* %# %++ @** *-** *-** **-*** **-*** **-*** @** @*** #% %% %++ %++ %++ %++ %# *+** %++ @** @* %# *+** @*** ## %% @*** 
{% endcodeblock %}

From the word "eso" in title and the unfriendly language showing above, we could guess this challenge is about esoteric language. Then, the hardest part of the challenge is to figure out what the fuck this language is. I luckily found out that the answer is [TapeBagel](https://esolangs.org/wiki/TapeBagel) by searching "tape" in [this](https://esolangs.org/wiki/Language_list) esoteric language list. This also explains why the file extension is ".tb".

Now all we need is to spend a few minutes understanding the language and either program an interpreter or use human interpreter. I chose the latter and recorded the process as below.

{% codeblock lang:plain line_number:false %}
inst: ##     inst: %%     inst: %++    inst: %++    inst: %++
int: [0] 0 0 int: [0] 0 0 int: [1] 0 0 int: [2] 0 0 int: [3] 0 0
output:      output:      output:      output:      output:     

inst: %#     inst: *&*    inst: @**    inst: %#     inst: **&*
int: 3 [0] 0 int: 3 [9] 0 int: 3 [9] 0 int: 3 9 [0] int: 3 9 [27]
output:      output:      output: I    output: I    output: I   

inst: ***-*   inst: ***-*   inst: %++     inst: %++
int: 3 9 [24] int: 3 9 [21] int: 3 9 [22] int: 3 9 [23]
output: I     output: I     output: I     output: I   

inst: @***    inst: *-*    inst: @***   inst: @**
int: 3 9 [23] int: 3 9 [0] int: 3 9 [0] int: 3 9 [0]
output: IW    output: IW   output: IW_  output: IW_I  

inst: *+**    inst: @***    inst: ***+*    inst: @***
int: 3 9 [12] int: 3 9 [12] int: 3 9 [15] int: 3 9 [15]
output: IW_I  output: IW_IL output: IW_IL output: IW_ILO  

inst: **+**    inst: ***+*    inst: %++     inst: @***
int: 3 9 [18]  int: 3 9 [21]  int: 3 9 [22] int: 3 9 [22]
output: IW_ILO output: IW_ILO output: IW_IL output: IW_ILOV 

inst: #%        inst: %%        inst: %++       inst: %++
int: 1 1 [1]    int: [1] 1 1    int: [2] 1 1    int: [3] 1 1
output: IW_ILOV output: IW_ILOV output: IW_ILOV output: IW_ILOV 

inst: %++       inst: %++       inst: @*         inst: %#
int: [4] 1 1    int: [5] 1 1    int: [5] 1 1     int: 5 [1] 1
output: IW_ILOV output: IW_ILOV output: IW_ILOVE output: IW_ILOVE

inst: %++        inst: %++        inst: %++        inst: %%
int: 5 [2] 1     int: 5 [3] 1     int: 5 [4] 1     int: [5] 4 1
output: IW_ILOVE output: IW_ILOVE output: IW_ILOVE output: IW_ILOVE

inst: *&**       inst: @*          inst: @***         inst: *-**
int: [20] 4 1    int: [20] 4 1     int: [20] 4 1      int: [16] 4 1
output: IW_ILOVE output: IW_ILOVET output: IW_ILOVETA output: IW_ILOVETA

inst: @*            inst: %#            inst: %++
int: [16] 4 1       int: 16 [4] 1       int: 16 [5] 1
output: IW_ILOVETAP output: IW_ILOVETAP output: IW_ILOVETAP

inst: @**            inst: *-**           inst: *-**
int: 16 [5] 1        int: 16 [11] 1       int: 16 [5] 1
output: IW_ILOVETAPE output: IW_ILOVETAPE output: IW_ILOVETAPE

inst: **-***         inst: **-***         inst: **-***
int: 16 [4] 1        int: 16 [3] 1        int: 16 [2] 1
output: IW_ILOVETAPE output: IW_ILOVETAPE output: IW_ILOVETAPE

inst: @**             inst: @***             inst: #%
int: 16 [2] 1         int: 16 [2] 1          int: 1 [1] 1
output: IW_ILOVETAPEB output: IW_ILOVETAPEBA output: IW_ILOVETAPEBA

inst: %%               inst: %++              inst: %++
int: [1] 1 1           int: [2] 1 1           int: [3] 1 1
output: IW_ILOVETAPEBA output: IW_ILOVETAPEBA output: IW_ILOVETAPEBA

inst: %++              inst: %++              inst: %#
int: [4] 1 1           int: [5] 1 1           int: 5 [1] 1
output: IW_ILOVETAPEBA output: IW_ILOVETAPEBA output: IW_ILOVETAPEBA

inst: *+**             inst: %++              inst: @**
int: 5 [6] 1           int: 5 [7] 1           int: 5 [7] 1
output: IW_ILOVETAPEBA output: IW_ILOVETAPEBA output: IW_ILOVETAPEBAG

inst: @*                 inst: %#
int: 5 [7] 1             int: 5 7 [1]
output: IW_ILOVETAPEBAGE output: IW_ILOVETAPEBAGE

inst: *+**               inst: @***
int: 5 7 [12]            int: 5 7 [12]
output: IW_ILOVETAPEBAGE output: IW_ILOVETAPEBAGEL

inst: ##                  inst: %%
int: 0 0 [0]              int: [0] 0 0
output: IW_ILOVETAPEBAGEL output: IW_ILOVETAPEBAGEL

inst: @***
int: [0] 0 0
output: IW_ILOVETAPEBAGEL_
{% endcodeblock %}

The flag can be easily guessed during the halfway of interpretation.

> Flag: `IW{ILOVETAPEBAGEL}`
