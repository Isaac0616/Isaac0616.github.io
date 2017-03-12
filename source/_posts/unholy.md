---
title: 'Boston Key Party CTF 2016: unholy (reversing 4)'
tags:
  - x86-64
  - python
  - ruby
  - reverse
  - Boston Key Party CTF
categories:
  - writeup
date: 2016-03-10 23:48:02
---


## Description

> python or ruby? why not both! 
> {% asset_link 9c2b8593c64486de25698fcece7c12fa0679a224.tar.gz https://s3.amazonaws.com/bostonkeyparty/2016/9c2b8593c64486de25698fcece7c12fa0679a224.tar.gz %}

## Exploit

This challenge involves three languages: Ruby, Python, and x86-64 assembly. They are combined by some kind of native extension mechanism, but we don't have to understand the details of the mechanism nor master these languages to solve the problem. Just make the best guess and verify it. First, have a look at the main program.

{% include_code lang:ruby main.rb %}

The methods used in `main.rb` can be found in `unholy.so`. Here is the piece of code that register the Ruby module and methods.

{% codeblock lang:x86asm line_number:false %}
void __cdecl Init_unholy()
push    rbx
lea     rdi, aUnholy    ; "UnHoly"
call    _rb_define_module
mov     rbx, cs:UnHoly_ptr
lea     rdx, method_python_hi
lea     rsi, aPython_hi ; "python_hi"
mov     rdi, rax
xor     ecx, ecx
mov     [rbx], rax
call    _rb_define_method
mov     rdi, [rbx]
lea     rdx, method_ruby_hi
lea     rsi, aRuby_hi   ; "ruby_hi"
xor     ecx, ecx
call    _rb_define_method
mov     rdi, [rbx]
lea     rdx, method_check_key
lea     rsi, aIs_key_correct ; "is_key_correct?"
pop     rbx
mov     ecx, 1
jmp     _rb_define_method
{% endcodeblock %}

The main program want us to enter the flag, and then it will unpack the input string into integer array and pass it to the method `is_key_correct?`. According to `Init_unholy` above, we should look into `method_check_key` now. `method_check_key` can be divided into three parts.

{% codeblock Part1 lang:c %}
v2 = *(_QWORD *)payload;
if ( BYTE1(v2) & 0x20 )
  v3 = (v2 >> 15) & 3;
else
  v3 = *(_DWORD *)(payload + 16);

key[0] = 'tahw';
key[1] = 'iogs';
key[2] = 'nogn';
key[3] = 'ereh';

if ( v3 == 9 )
{
  v4 = 0LL;
  do {
    LODWORD(v5) = rb_ary_entry(payload, v4);
    if ( v5 & 1 )
      v6 = rb_fix2int(v5);
    else
      v6 = rb_num2int(v5);
    matrix[v4++] = v6;
  } while ( v4 != 9 );
  matrix[9] = 1634947872;
  ...
{% endcodeblock %}

I have spent some time investigating why it check whether the first byte of the payload is `0x20`, what `rb_ary_entry`, `rb_fix2int`, and `rb_num2int` do, and so on. However, they are quite irrelevant. They are all about the memory representation of Ruby's data structure (e.g. the first byte of the payload is the length of the Ruby's array). Using `gdb`, we can directly find out what Part1 does is putting our input (in integer array format) into `matrix` and initialize some other data.

{% codeblock Part2 lang:c %}
...
v7 = 0LL;
do {
  v8 = 0;
  LODWORD(v9) = *(_QWORD *)&matrix[v7];
  v10 = *(_QWORD *)&matrix[v7] >> 32;
  do {
    v11 = v8 + key[(unsigned __int64)(v8 & 3)];
    v8 -= 1640531527;
    v9 = (v11 ^ ((16 * (_DWORD)v10 ^ ((unsigned int)v10 >> 5)) + (_DWORD)v10)) + (unsigned int)v9;
    v10 = ((v8 + key[(unsigned __int64)((v8 >> 11) & 3)]) ^ ((16 * (_DWORD)v9 ^ ((unsigned int)v9 >> 5)) + (_DWORD)v9))
        + (unsigned int)v10;
  } while ( v8 != -957401312 );
  *(_QWORD *)&matrix[v7] = v9 | (v10 << 32);
  v7 += 2LL;
} while ( v7 != 10 );
...
{% endcodeblock %}

In Part2, it applys some operations on `matrix` (our input) and `key` (known data) two entries at a time. It look messy at the first glance, but the operations can actually be inverted. Values derived from `v8` are constant, so we know that the inner loop will iterate 32 times and the operation can be simplify as

{% codeblock Part2 lang:python %}
for i in range(32):
    v9 = (C ^ (16*v10 ^ (v10 >> 5)) + v10) + v9
    v10 = (C ^ (16*v9 ^ (v9 >> 5)) + v9) + v10
{% endcodeblock %}

where `C` stands for known constant. We can calculate `v10` of the previous loop by current `v10` and `v9`, and then we can use previous `v10` and current `v9` to calculate previous `v9`. Following this process, we can get the initial `v9` and `v10`.

{% codeblock Part3 lang:c %}
  ...
  if ( matrix[9] == 1306786301 )
  {
    __sprintf_chk(
      stacker,
      1LL,
      5000LL,
      "exec \"\"\"\\nimport struct\\ne=range\\nI=len\\nimport sys\\nF=sys.exit\\nX=[[%d,%d,%d],[%d,%d,%d],[%d,%d,%d]]\\nY = [[383212,38297,8201833],[382494 ,348234985,3492834886],[3842947 ,984328,38423942839]]\\nn=[5034563854941868,252734795015555591,55088063485350767967,-2770438152229037,142904135684288795,-33469734302639376803,-3633507310795117,195138776204250759,-34639402662163370450]\\ny=[[0,0,0],[0,0,0],[0,0,0]]\\nA=[0,0,0,0,0,0,0,0,0]\\nfor i in e(I(X)):\\n for j in e(I(Y[0])):\\n  for k in e(I(Y)):\\n   y[i][j]+=X[i][k]*Y[k][j]\\nc=0\\nfor r in y:\\n for x in r:\\n  if x!=n[c]:\\n   print \"dang...\"\\n   F(47)\\n  c=c+1\\nprint \":)\"\\n\"\"\"",
      matrix[0],
      matrix[1]);
    Py_Initialize(stacker, 1LL);
    PyRun_SimpleStringFlags(stacker, 0LL);
    Py_Finalize(stacker, 0LL);
  }
}
{% endcodeblock %}

The parameters of `sprintf` is incorrect in the decompiled code, but it suggests that Part3 prints the values in `matrix` into following Python code and execute it.

{% codeblock lang:python %}
      exec """
      import struct
      e=range
      I=len
      import sys
      F=sys.exit

      X=[[%d,%d,%d],[%d,%d,%d],[%d,%d,%d]]
      Y = [[383212,38297,8201833],[382494 ,348234985,3492834886],[3842947 ,984328,38423942839]]
      n=[5034563854941868,252734795015555591,55088063485350767967,-2770438152229037,142904135684288795,-33469734302639376803,-3633507310795117,195138776204250759,-34639402662163370450]
      y=[[0,0,0],[0,0,0],[0,0,0]]
      A=[0,0,0,0,0,0,0,0,0]

      for i in e(I(X)):
          for j in e(I(Y[0])):
              for k in e(I(Y)):
                  y[i][j]+=X[i][k]*Y[k][j]

      c=0
      for r in y:
          for x in r:
              if x!=n[c]:
                  print "dang..."
                  F(47)
              c=c+1
      print ":)"
      """
{% endcodeblock %}

This Python code multiplies two matrices. We can solve it by inverse matrix or using Z3.

Combining the reversing process of Part2 and Part3, we can use following Python script to get the flag. 

{% include_code lang:python solve.py %}

`&0xffffffff` which scatters in the script is to simulate integer overflow.

> Flag: `BKPCTF{hmmm _why did i even do this}`

## Note
1. It seems that Python doesn't provide a handy way to compute integer with overflow.
2. I try to solve Part2 by Z3 at the beginning, but it hang forever. Sometimes we should just settle down to read the code and get our hands dirty. Don't depend on tools too much.
3. I debug by `gdb --args ruby main.rb`, but it is hard to set breakpoints in a shared library. Maybe there is a better way to debug.
4. According to other people's writeup, the Part2 is actually doing XTEA cipher. The clue is lots of xor and shift operations which implie it is performing some kind of cipher. By googling the constant `0xc6ef3720`, we can find out that the answer is XTEA.
