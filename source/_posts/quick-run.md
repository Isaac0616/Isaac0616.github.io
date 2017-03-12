---
title: 'Internetwache CTF 2016: Quick Run (misc 60)'
tags:
  - misc
  - Internetwache CTF
categories:
  - writeup
date: 2016-02-25 12:43:38
---


## Description

> Someone sent me a file with white and black rectangles. I don't know how to read it. Can you help me?
> **Attachment:** {% asset_link misc60.zip %}

## Exploit

Since the `=` padding in the `README.txt`, I try to use base64 decode and get something like

{% codeblock lang:plain line_number:false %}
██████████████████████████████████████████████
██              ██  ██  ██  ██              ██
██  ██████████  ██████████  ██  ██████████  ██
██  ██      ██  ██  ████    ██  ██      ██  ██
██  ██      ██  ██████████  ██  ██      ██  ██
██  ██      ██  ██  ████  ████  ██      ██  ██
██  ██████████  ████    ██  ██  ██████████  ██
██              ██  ██  ██  ██              ██
████████████████████████    ██████████████████
████  ████  ██  ████    ██    ████  ██  ██  ██
██            ██    ████████  ██  ████████  ██
██  ██  ██████            ████████  ██  ██  ██
██  ████  ██  ██  ██  ██  ██  ██  ██  ██  ████
████  ██    ██  ██  ██  ██  ██  ██  ██  ██  ██
████████████████████  ██  ██  ██  ██  ██  ████
██              ██████  ██  ██  ██  ██  ██  ██
██  ██████████  ████  ██  ██  ██  ██  ██  ████
██  ██      ██  ██  ██  ██  ██  ██  ██  ██  ██
██  ██      ██  ████  ██  ██  ██  ██  ██  ████
██  ██      ██  ██████  ██  ██  ██  ██  ██  ██
██  ██████████  ██    ██    ████  ██  ██  ████
██              ██████    ████████  ██      ██
██████████████████████████████████████████████
{% endcodeblock %}

It is clear that they are QR code. However, I can't scan the QR code in the text format even I adjust the line hight and change the color into black and white. Therefore, I write a script to get the message. I use `PIL` to create the QR code image and scan it by `zbarlight`. (Actually, during the competition, I simply show the QR code and scan by my mobile.) The message is `Flagis:IW{QR_C0DES_RUL3}`.

{% include_code lang:python decode.py %}

> Flag: `IW{QR_C0DES_RUL3}`
