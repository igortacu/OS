#!/usr/bin/env python3
"""Reproduce only the deliberately incorrect variants required by Lab 12."""
from pathlib import Path

root = Path(__file__).resolve().parent
out = root / 'variants'
out.mkdir(exist_ok=True)

def replace_once(text, old, new):
    assert text.count(old) == 1, f'Expected one occurrence of {old!r}'
    return text.replace(old, new, 1)

producer = (root / 'prodcons.c').read_text()
producer = replace_once(producer,
    '        sem_wait(&empty);\n        pthread_mutex_lock(&lock);',
    '        pthread_mutex_lock(&lock);\n        sem_wait(&empty);')
(out / 'prodcons_bad.c').write_text(producer)

condition = replace_once((root / 'condvar.c').read_text(),
                         'while (!ready)', 'if (!ready)')
(out / 'condvar_if.c').write_text(condition)

fixed = (root / 'deadlock.c').read_text()
start = fixed.index('void *two(')
end = fixed.index('\nint main(', start)
two = fixed[start:end]
two = replace_once(two, 'pthread_mutex_lock(&A);', 'pthread_mutex_lock(&B);')
# The second lock was originally B; replace that specific surrounding context.
two = replace_once(two, 'sleep(1);\n    pthread_mutex_lock(&B);',
                   'sleep(1);\n    pthread_mutex_lock(&A);')
two = two.replace('two: I have A, I want B', 'two: I have B, I want A')
two = replace_once(two,
    'pthread_mutex_unlock(&B);\n    pthread_mutex_unlock(&A);',
    'pthread_mutex_unlock(&A);\n    pthread_mutex_unlock(&B);')
bad = fixed[:start] + two + fixed[end:]
bad = bad.replace('FIXED version. Both threads acquire A before B.',
                  'INCORRECT variant. Threads acquire the mutexes in opposite order.')
(out / 'deadlock_bad.c').write_text(bad)
(out / 'deadlock_nosleep.c').write_text(bad.replace('    sleep(1);\n', ''))
print('Created prodcons_bad, condvar_if, deadlock_bad, deadlock_nosleep sources.')
