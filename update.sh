#!/bin/bash
cd $(dirname ${0})
source venv/bin/activate
python update_ticker_data_db.py
