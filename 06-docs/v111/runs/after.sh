#!/bin/bash
# after.sh <wait-log> <jobs> <log>: wait until the wait-log's lane has finished, then run the jobs lane.
until grep -q "LANE FINISHED" "$1"; do sleep 5; done
bash "$(dirname "$0")/lane.sh" "$2" "$3"
