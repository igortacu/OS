#include "kernel/types.h"
#include "kernel/stat.h"
#include "kernel/fs.h"
#include "kernel/fcntl.h"
#include "user/user.h"

static char *
basename(char *path)
{
  char *last = path;
  for(char *p = path; *p; p++)
    if(*p == '/') last = p + 1;
  return last;
}

static int
visit(char *path, char *target)
{
  struct stat st;
  if(stat(path, &st) < 0){
    fprintf(2, "find: cannot stat %s\n", path);
    return 1;
  }
  // A directory can match as well as a regular file.
  if(strcmp(basename(path), target) == 0) printf("%s\n", path);
  if(st.type != T_DIR) return 0;

  int fd = open(path, O_RDONLY);
  if(fd < 0){
    fprintf(2, "find: cannot open %s\n", path);
    return 1;
  }
  struct dirent de;
  char child[512], name[DIRSIZ + 1];
  int failed = 0, n;
  while((n = read(fd, &de, sizeof(de))) == sizeof(de)){
    if(de.inum == 0) continue;
    memmove(name, de.name, DIRSIZ);
    name[DIRSIZ] = 0;
    if(strcmp(name, ".") == 0 || strcmp(name, "..") == 0) continue;
    if(strlen(path) + strlen(name) + 2 > sizeof(child)){
      fprintf(2, "find: path too long under %s\n", path);
      failed = 1;
      continue;
    }
    strcpy(child, path);
    strcpy(child + strlen(child), "/");
    strcpy(child + strlen(child), name);
    failed |= visit(child, target);
  }
  if(n != 0){
    fprintf(2, "find: directory read failed for %s\n", path);
    failed = 1;
  }
  close(fd);
  return failed;
}

int
main(int argc, char **argv)
{
  if(argc != 3){
    fprintf(2, "usage: find start basename\n");
    exit(1);
  }
  exit(visit(argv[1], argv[2]));
}
