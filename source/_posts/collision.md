---
title: 'Pwnable.kr: collision (3 pt)'
tags:
  - Pwnable.kr
categories:
  - writeup
date: 2016-08-08 21:24:12
---


## Description

> Daddy told me about cool MD5 hash collision today.
> I wanna do something like that too!
> ssh col@pwnable.kr -p2222 (pw:guest)

## Exploit

{% codeblock fd.c lang:c %}
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
{% endcodeblock %}

The target program converts the argument from a 20 bytes string to an array of 5 integers and sum them up. If the sum equals to `0x21DD09EC`, it will output the flag. I craft the input with 4 integers of `\x01\x01\x01\x01` (just for padding) plus an integer of the difference to the target hashcode. The difference can be calculated as follows.

{% include_code lang:python cal.py %}

After calculating the difference, which is `\xe8\x05\xd9\x1d`, we can solve the problem with the input mentioned above.

{% codeblock lang:plain line_number:false %}
$ ./col $'\xe8\x05\xd9\x1d\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
daddy! I just managed to create a hash collision :)
{% endcodeblock %}

> Flag: `daddy! I just managed to create a hash collision :)`
