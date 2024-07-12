#!/bin/bash
cd "$(dirname ${0})" || exit
source venv/bin/activate

# daily data update for trade
python unit_update_table_trade_daily.py

# daily report
# python report_correlation_7735.py
# python report_correlation_8035.py
python report_correlation_8306.py

# python report_sector_close_daily.py
# python report_sector_close_open_daily.py
python report_sector_change_ratio_daily.py
cd /home/bitwalk/MyProjects/stock || exit
git pull
git add report/*/*.png
git commit -m "update"
git push
