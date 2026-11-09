#!/bin/bash
if [ "$#" -ne 1 ]; then
    printf 'usage: %s readable_log\n' "$0" >&2
    exit 1
fi
if [ ! -f "$1" ] || [ ! -r "$1" ]; then
    printf 'no such file: %s\n' "$1" >&2
    exit 1
fi
awk '
  { total++ }
  $4 == "FAIL" { failed++; by_user[$3]++ }
  END {
    printf "%d requests, %d failed\n", total, failed
    for (i=0; i<7; i++) printf "user%d: %d failures\n", i, by_user["user" i]
  }
' "$1"
