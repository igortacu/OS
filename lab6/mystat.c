#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int
main(int argc, char **argv)
{
  if(argc < 2){
    fprintf(2, "usage: mystat path ...\n");
    exit(1);
  }
  int failed = 0;
  for(int i = 1; i < argc; i++){
    struct stat st;
    if(stat(argv[i], &st) < 0){
      fprintf(2, "mystat: cannot stat %s\n", argv[i]);
      failed = 1;
      continue;
    }
    char *kind = st.type == T_DIR ? "directory" :
                 st.type == T_FILE ? "file" :
                 st.type == T_DEVICE ? "device" : "unknown";
    printf("%s: type=%s inode=%d links=%d bytes=%lu\n",
           argv[i], kind, st.ino, st.nlink, st.size);
  }
  exit(failed);
}
