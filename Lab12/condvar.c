/* Lab 12: the predicate remembers readiness; the condition wakes waiters. */
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

char message[32];
int ready = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t changed = PTHREAD_COND_INITIALIZER;

void *writer(void *arg)
{
    (void)arg;
    sleep(1);
    pthread_mutex_lock(&lock);
    strcpy(message, "hello");
    ready = 1;
    printf("A: message written\n");
    pthread_cond_signal(&changed);
    pthread_mutex_unlock(&lock);
    return NULL;
}

void *reader(void *arg)
{
    (void)arg;
    pthread_mutex_lock(&lock);
    while (!ready) {
        printf("B: not ready, I sleep\n");
        pthread_cond_wait(&changed, &lock);
    }
    printf("B: I read \"%s\"\n", message);
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main(void)
{
    pthread_t a, b;
    pthread_create(&b, NULL, reader, NULL);
    pthread_create(&a, NULL, writer, NULL);
    pthread_join(a, NULL);
    pthread_join(b, NULL);
    pthread_cond_destroy(&changed);
    pthread_mutex_destroy(&lock);
    return 0;
}
