/* Lab 9: observe open, write, read, and close with strace. */
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(void)
{
    const char *msg = "hello, kernel\n";
    int fd = open("note.txt", O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open for writing");
        return 1;
    }

    printf("open returned descriptor %d\n", fd);
    ssize_t n = write(fd, msg, strlen(msg));
    if (n < 0 || (size_t)n != strlen(msg)) {
        perror("write");
        close(fd);
        return 1;
    }
    printf("write sent %zd bytes\n", n);
    if (close(fd) < 0) {
        perror("close after writing");
        return 1;
    }

    fd = open("note.txt", O_RDONLY);
    if (fd < 0) {
        perror("open for reading");
        return 1;
    }
    char buf[64];
    n = read(fd, buf, sizeof(buf) - 1);
    if (n < 0) {
        perror("read");
        close(fd);
        return 1;
    }
    buf[n] = '\0';
    printf("read got %zd bytes: %s", n, buf);
    if (close(fd) < 0) {
        perror("close after reading");
        return 1;
    }
    return 0;
}
