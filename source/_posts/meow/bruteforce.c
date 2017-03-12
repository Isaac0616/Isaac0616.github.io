#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>

const char* TARGET = "\x9f\x46\xa9\x24\x22\x65\x8f\x61\xa8\x0d\xde\xe7\x8e\x7d\xb9\x14";

int main() {
  unsigned char result[MD5_DIGEST_LENGTH];

  char string[11] = {0};

  for(unsigned char i = 0x20; i <= 0x7e; i++) {
      printf("input[2] = 0x%02x\n", i);
      for(unsigned char j = 0x20; j <= 0x7e; j++) {
          for(unsigned char k = 0x20; k <= 0x7e; k++) {
              for(unsigned char l = 0x20; l <= 0x7e; l++) {
                  string[2] = i;
                  string[5] = string[2] ^ 0b01011000;
                  string[3] = string[2];
                  string[9] = string[3] ^ 0b01001010;
                  string[1] = string[3] ^ 0b01100100;
                  string[8] = string[1] ^ 0b01111100;
                  string[0] = string[1] ^ 0b01110011;

                  string[4] = j;
                  string[6] = k;
                  string[7] = l;

                  MD5(string, 10, result);
                  if(strncmp(result, TARGET, 16) == 0) {
                      printf("%s\n", string);
                  }
              }
          }
      }
  }

  return 0;
}
