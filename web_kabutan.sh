#!/bin/bash
cd "$(dirname ${0})" || exit
source venv/bin/activate
python web_kabutan_good_bad.py
