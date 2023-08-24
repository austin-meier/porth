#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

void dump(uint64_t x) {
  char buffer[32];
  size_t idx = 1;
  buffer[sizeof(buffer) - idx] = '\n';

   do {
    buffer[sizeof(buffer) - idx - 1] = x % 10 + '0';
    idx++;
    x /= 10;
  } while(x);

  write(1, &buffer[sizeof(buffer) - idx], idx);
}

int main() {
  dump(69420);
  dump(0);
  return 0;
}