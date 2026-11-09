#include "kernel/types.h"
#include "user/user.h"

int
main(int argc, char **argv)
{
  if(argc != 2 || argv[1][0] == 0){
    fprintf(2, "usage: sleep nonnegative_ticks\n");
    exit(1);
  }
  int ticks = 0;
  for(char *p = argv[1]; *p; p++){
    if(*p < '0' || *p > '9' || ticks > (2147483647 - (*p - '0')) / 10){
      fprintf(2, "sleep: invalid tick count\n");
      exit(1);
    }
    ticks = ticks * 10 + (*p - '0');
  }
  exit(pause(ticks) < 0);
}
