#!/bin/bash
source /home/pi/dev/virtualenv/hurlo/bin/activate
cd /home/pi/dev/hurlomaton
python3 0_hardware_check.py &&
hardware = $!
wait[$!] &
python3 1_crop_watch.py &
python3 3_hurlomaton.py