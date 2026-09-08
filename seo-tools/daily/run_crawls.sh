#!/bin/bash
cd "$(dirname "$0")"
SITES=$(python3 -c "from _sites import SITES; [print(s,c) for s,_,c in SITES]")
pids=()
while read slug host; do
  ( python3 crawler.py "$slug" "$host" > "crawl_$slug.log" 2>&1 ) &
  pids+=($!)
done <<< "$SITES"
for p in "${pids[@]}"; do wait "$p"; done
for f in crawl_*.log; do printf "%-18s %s\n" "$f" "$(tail -1 "$f")"; done
echo ALL-CRAWLS-DONE
