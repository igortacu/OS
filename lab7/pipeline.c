#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int delay_eof = argc == 2 && strcmp(argv[1], "--delay-eof") == 0;
    if (argc > 1 && !delay_eof) {
        fprintf(stderr, "usage: %s [--delay-eof]\n", argv[0]);
        return 2;
    }

    int p[2];
    if (pipe(p) < 0) {
        perror("pipe");
        return 1;
    }
    pid_t ls_pid = fork();
    if (ls_pid < 0) {
        perror("fork");
        return 1;
    }
    if (ls_pid == 0) {
        close(STDOUT_FILENO);
        if (dup(p[1]) != STDOUT_FILENO) _exit(1);
        close(p[0]);
        close(p[1]);
        execlp("ls", "ls", "/etc", (char *)NULL);
        perror("exec ls");
        _exit(127);
    }

    pid_t wc_pid = fork();
    if (wc_pid < 0) {
        perror("fork");
        close(p[0]);
        close(p[1]);
        waitpid(ls_pid, NULL, 0);
        return 1;
    }
    if (wc_pid == 0) {
        close(STDIN_FILENO);
        if (dup(p[0]) != STDIN_FILENO) _exit(1);
        close(p[0]);
        close(p[1]);
        execlp("wc", "wc", "-l", (char *)NULL);
        perror("exec wc");
        _exit(127);
    }

    close(p[0]);
    if (delay_eof) {
        fprintf(stderr, "parent keeps the write end open for 3 seconds; wc waits for EOF\n");
        sleep(3);
    }
    close(p[1]);
    int ls_status, wc_status;
    if (waitpid(ls_pid, &ls_status, 0) < 0 || waitpid(wc_pid, &wc_status, 0) < 0) {
        perror("waitpid");
        return 1;
    }
    return WIFEXITED(ls_status) && WEXITSTATUS(ls_status) == 0 &&
           WIFEXITED(wc_status) && WEXITSTATUS(wc_status) == 0 ? 0 : 1;
}
