#!/bin/bash
cd "$(dirname ${0})" || exit
source venv/bin/activate
python dta_uploader_1m.py
