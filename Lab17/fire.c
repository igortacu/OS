/* Lab 17 baseline: deliberately racy, following the supplied handout.
 * Build without optimization for the observation, not for correctness.
 * Concurrent unsynchronized accesses are undefined behavior in C. */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef THREADS
#define THREADS 2
#endif
#define N 1000000
long counter = 0;

static void *work(void *arg)
{
    long id = *(long *)arg;
    printf("thread %ld sees counter = %ld\n", id, counter);
    for (int i = 0; i < N; i++)
        counter++;                 /* deliberately NOT atomic */
    return NULL;
}

int main(void)
{
    pthread_t threads[THREADS];
    long ids[THREADS];
    for (int i = 0; i < THREADS; i++) {
        ids[i] = i + 1;
        int error = pthread_create(&threads[i], NULL, work, &ids[i]);
        if (error) {
            fprintf(stderr, "pthread_create: %s\n", strerror(error));
            exit(1);
        }
    }
    for (int i = 0; i < THREADS; i++) {
        int error = pthread_join(threads[i], NULL);
        if (error) {
            fprintf(stderr, "pthread_join: %s\n", strerror(error));
            exit(1);
        }
    }
    printf("expected: %d\n", THREADS * N);
    printf("counter: %ld    (lost updates: the race)\n", counter);
    return 0;
}
