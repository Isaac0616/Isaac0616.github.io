---
title: 'IceCTF 2016: Attack of the Hellman! (crypto 175)'
tags:
  - IceCTF
  - crypto
categories:
  - writeup
---

## Description

> We managed to intercept a flag transmission but it was encrypted :(. We got the {% asset_link scripts_7c80a737ea110ce8b552443ffb0f143db314d05a1704a7391eb5c86aadf8feb2.zip Diffie-Hellman public key exchange parameters %} and some {% asset_link scripts_7c80a737ea110ce8b552443ffb0f143db314d05a1704a7391eb5c86aadf8feb2.zip scripts %} they used for the transmission along with the {% asset_link flag_c5a6c6e0fe9d7ab6785c0886c13a49a4bbe799d1bd3413333a35f1e86e549de5.enc encrypted flag %}. Can you get it for us? )

## Exploit

First, I look into the provided files.

- **public:** the Diffie-Hellman parameters
- **flag.enc:** encrypted flag
- **scripts**
    - **generate_dh.sage/dh_exchange.sage:** carry out Diffie-Hellman protocol
    - **encrypt/decrypt:** encrypt/decrypt the flag using aes-256-cbc of OpenSSL 



## Summary
