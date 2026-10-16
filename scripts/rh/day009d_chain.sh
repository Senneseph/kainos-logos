#!/usr/bin/env bash
# day009d_chain.sh — unattended chain:
#   1) GPU flip walk 1e5->6e6 (day009b, streaming segments)
#   2) as soon as segment [1e5,3e5) completes both passes, merge the G=3e5
#      list and run the onset rerun (day009c) on the host (mpmath).
set -u
cd /home/jsmille/Projects/kainos-logos/scripts/rh
LOG=out_day009b_zero_walk_1e5_6e6_gpu.txt
nohup ~/venvs/cupy/bin/cupy_py -u day009b_zero_walk_1e5_6e6_gpu.py \
    > "$LOG" 2>&1 &
WALKPID=$!
echo "walk pid $WALKPID log $LOG"
SEG=flips_seg_00100000_00300000_dt2.txt
while true; do
  sleep 90
  if [ -f "$SEG" ]; then
    if ! kill -0 "$WALKPID" 2>/dev/null; then
      echo "walk died before segment completed — chain aborting"
      break
    fi
    echo "segment [1e5,3e5) present — merging G=3e5 list, launching onset rerun"
    cat zeros_T100000.txt "$SEG" > zeros_T300000_ext_full.txt
    nohup python3 -u day009c_onset_pred_ext.py zeros_T300000_ext_full.txt \
        > out_day009c_onset_pred_ext.txt 2>&1 &
    echo "onset rerun pid $!"
    break
  fi
done
wait "$WALKPID"
echo "walk finished (exit $?)"
