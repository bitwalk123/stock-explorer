#!/bin/bash
cd $(dirname ${0}) || exit
source venv/bin/activate
python update_ticker_data_db.py

python report_daily_sector.py
cd /home/bitwalk/MyProjects/stock || exit
git add report/*/*.png
git commit -m "update"
git push
