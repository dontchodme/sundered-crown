#!/bin/bash
# lane.sh <jobs-file> <log>: run each line of the jobs file in order (one browser at a time),
# from C:/dev/sundered-crown/tools, and log START/DONE with the exit code.
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
while IFS= read -r line; do
  [ -z "$line" ] && continue
  case "$line" in \#*) continue;; esac
  echo "START $(date +%H:%M:%S) $line" >> "$2"
  bash -c "$line"
  echo "DONE rc=$? $(date +%H:%M:%S) $line" >> "$2"
done < "$1"
echo "LANE FINISHED $(date +%H:%M:%S)" >> "$2"
