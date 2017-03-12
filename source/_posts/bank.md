---
title: 'Internetwache CTF 2016: Bank (crypto 90)'
tags:
  - crypto
  - Internetwache CTF
  - xor
categories:
  - writeup
date: 2016-03-02 14:59:42
---

## Description

> Everyone knows that banks are insecure. This one super secure and only allows only 20 transactions per session. I always wanted a million on my account.
> **Attachment:** {% asset_link crypto90.zip %}

## Exploit

In this challenge, we have to deposit 1000000 dollars in the account within 20 transactions to get the flag. To complete a transaction, we have to first initiate it by providing how much we want to deposit. Then, use the "hashcode" it returns to finalize the transaction. The problem is that we can only deposit 5000 dollars at a time, so we must tamper the "hashcode" to deposit more money.

The vulnerability in this challenge is that the "hashcode" it returns is just the result of xoring the plain text and a key. Since we know what the plain text is, we can easily retrieve the key and use it to create a "hashcode" of our own content. I created 20 transactions of 99999 dollars to get the flag.

{% include_code lang:python exp.py %}

> Flag: `IW{SHUT_UP_AND_T4K3_MY_M000NEYY}`
