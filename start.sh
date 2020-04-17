#!/bin/bash
set -euxo pipefail

# Wait for the background NTP sync to complete by repeatedly checking if the
# time offset is within a comfortable threshold of 5 mins.
python wait_for_ntp_sync.py

# The Wifi scanning script
python mrtScanner.py
