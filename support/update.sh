#!/bin/bash
R CMD BATCH --vanilla --slave /home/bitwalk/shiny-app/stock-explorer/support/update.R
cd /home/bitwalk/shiny-app/stock-explorer/; git add stock-explorer.sqlite3; git commit -m "daily update"; git push
