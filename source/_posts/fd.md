---
title: 'Pwnable.kr: fd (1 pt)'
date: 2016-08-08 14:50:37
tags:
  - Pwnable.kr
categories:
  - writeup
---

## Description

> Mommy! what is a file descriptor in Linux?
> ssh fd@pwnable.kr -p2222 (pw:guest)

## Exploit

{% codeblock fd.c lang:c %}
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	int fd = atoi( argv[1] ) - 0x1234;
	int len = 0;
	len = read(fd, buf, 32);
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		system("/bin/cat flag");
		exit(0);
	}
	printf("learn about Linux file IO\n");
	return 0;

}
{% endcodeblock %}

The target program will read 32 bytes from file descriptor `argv[1] - 0x1234`, and if the content equals to `LETMEWIN\n`, it will output the flag. To solve this problem, we can pass 4660 (0x1234) as the first argument. Then this program will read from the standard input, which we can assign its value to `LETMEWIN\n` to get the flag.

{% codeblock lang:plain line_number:false %}
$ echo "LETMEWIN" | ./fd 4660
good job :)
mommy! I think I know what a file descriptor is!!
{% endcodeblock %}

> Flag: `mommy! I think I know what a file descriptor is!!`
