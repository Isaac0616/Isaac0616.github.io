---
title: 'Internetwache CTF 2016: Oh Bob! (crypto 60)'
tags:
  - crypto
  - Internetwache CTF
  - RSA
categories:
  - writeup
date: 2016-03-01 09:08:18
---

## Description

> Alice wants to send Bob a confidential message. They both remember the crypto lecture about RSA. So Bob uses openssl to create key pairs. Finally, Alice encrypts the message with Bob's public keys and sends it to Bob. Clever Eve was able to intercept it. Can you help Eve to decrypt the message?
> **Attachment:** {% asset_link crypto60.zip %}

## Exploit

The RSA keys are too short. They are only 228 bits that can be easily fatorized by [yafu](https://sourceforge.net/projects/yafu/). After fatorization, we can decrypt the messages use the RSA algorithm.

{% include_code lang:python publickey.py %}

{% include_code lang:python decrypt.py %}

> Flag: `IW{WEAK_RSA_K3YS_4R3_SO_BAD!}`
