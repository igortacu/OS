// Additional Lab 13 checks: bounds, count overflow, wake-all, killed waiter.
#include "kernel/types.h"
#include "user/user.h"

static void
check(int ok, char *what)
{
  if (!ok) {
    fprintf(2, "semcheck: FAIL %s\n", what);
    exit(1);
  }
}

int
main(void)
{
  check(sem_init(-1, 0) == -1 && sem_init(8, 0) == -1, "init id bounds");
  check(sem_down(-1) == -1 && sem_down(8) == -1, "down id bounds");
  check(sem_up(-1) == -1 && sem_up(8) == -1, "up id bounds");
  check(sem_init(7, -1) == -1, "negative initial count");
  check(sem_init(7, 0x7fffffff) == 0 && sem_up(7) == -1, "overflow guard");
  check(sem_down(7) == 0 && sem_up(7) == 0, "count at upper bound");
  check(sem_init(7, 2) == 0, "count two init");
  check(sem_down(7) == 0 && sem_down(7) == 0, "consume two permits");
  printf("semcheck: bounds and counting OK\n");

  check(sem_init(4, 0) == 0, "waiter init");
  for (int i = 0; i < 4; i++) {
    int pid = fork();
    check(pid >= 0, "fork waiter");
    if (pid == 0) {
      check(sem_down(4) == 0, "waiter down");
      exit(0);
    }
  }
  pause(10);
  for (int i = 0; i < 4; i++)
    check(sem_up(4) == 0, "post waiter permit");
  for (int i = 0; i < 4; i++) {
    int status = -99;
    check(wait(&status) > 0 && status == 0, "reap waiter");
  }
  printf("semcheck: four waiting children released OK\n");

  check(sem_init(6, 0) == 0, "kill waiter init");
  int pid = fork();
  check(pid >= 0, "fork killed waiter");
  if (pid == 0) {
    sem_down(6);
    exit(42); // The killed process should not reach user space here.
  }
  pause(10);
  check(kill(pid) == 0, "kill blocked waiter");
  int status = 0;
  check(wait(&status) == pid && status == -1, "killed waiter exits");
  printf("semcheck: killed blocked child reaped OK\n");
  printf("semcheck: OK\n");
  exit(0);
}
