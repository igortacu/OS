#!/usr/bin/env bash
log=${1:-access.log}
[ -r "$log" ] || { printf 'cannot read %s\n' "$log" >&2; exit 1; }
printf '\nQ1 failed requests\n'
# Q1. How many requests failed?
awk '$4 == "FAIL" {n++} END {print n+0}' "$log"
printf '\nQ2 distinct pages\n'
# Q2. How many different pages and which?
awk '{print $5}' "$log" | sort -u | awk '{names[NR]=$0} END {print NR " distinct pages"; for(i=1;i<=NR;i++) print names[i]}'
printf '\nQ3 requests per page\n'
# Q3. How many requests did each page receive?
awk '{n[$5]++} END {for(p in n) print n[p],p}' "$log" | sort -k1,1nr -k2
printf '\nQ4 most failures\n'
# Q4. Which users tie for the most failures?
awk '$4 == "FAIL" {n[$3]++} END {for(u in n) if(n[u]>m)m=n[u]; for(u in n) if(n[u]==m) print u,n[u]}' "$log" | sort
printf '\nQ5 user3\n'
# Q5. How many requests and failures for user3?
awk '$3 == "user3" {n++; if($4=="FAIL")f++} END {printf "user3: %d requests, %d failed\n",n,f}' "$log"
printf '\nQ6 last three failures\n'
# Q6. Show the time and user of the last three failures.
awk '$4 == "FAIL" {print $2,$3}' "$log" | tail -3
printf '\nQ7 login shells\n'
# Q7. Count accounts grouped by login shell.
cut -d: -f7 /etc/passwd | sort | uniq -c | sort -nr
printf '\nQ8 directory listing line counts\n'
# Q8. Compare plain and long listing line counts.
ls /etc | wc -l
ls -l /etc | wc -l
