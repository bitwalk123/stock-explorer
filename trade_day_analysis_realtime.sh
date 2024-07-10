#!/bin/bash
cd "$(dirname ${0})" || exit
source venv/bin/activate
python trade_day_analysis_realtime.py
