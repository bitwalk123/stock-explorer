#!/bin/bash
cd "$(dirname ${0})" || exit
source venv/bin/activate
python news.py
