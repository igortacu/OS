#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    const char *program = argc > 1 ? argv[1] : "ls";
    printf("parent: my PID is %d\n", getpid());
    fflush(stdout);

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return 1;
    }
    if (pid == 0) {
        printf("child: my PID is %d, my parent is %d\n", getpid(), getppid());
        fflush(stdout);
        if (argc > 1)
            execvp(program, &argv[1]);
        else
            execlp("ls", "ls", "-l", (char *)NULL);
        perror("exec");
        _exit(127);
    }

    int status;
    if (waitpid(pid, &status, 0) < 0) {
        perror("waitpid");
        return 1;
    }
    if (WIFEXITED(status))
        printf("parent: child %d ended with status %d\n", pid, WEXITSTATUS(status));
    else if (WIFSIGNALED(status))
        printf("parent: child %d ended by signal %d\n", pid, WTERMSIG(status));
    return 0;
}
