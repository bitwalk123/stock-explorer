#!/bin/bash
cd "$(dirname ${0})" || exit
source venv/bin/activate

# daily data update for exchange
python unit_update_table_exchange_daily.py
python unit_update_itrade_daily.py
