# stock-explorer

This application is for predicting tomorrow's open price of specific stocks in Japan market using various machine learning algorithms.


![PREVIEW](preview.png) 

## Environment

- OS
  - CentOS 8

- Language
  - R/Shiny
    - for Shiny App
      - doParallel
      - Metrics
      - shiny
      - shinycssloaders
      - shinydashboard
      - shinyEventLogger
      - shinyjs
      - shinyWidgets
      - dplyr
      - DT
      - ggplot2
      - RSQLite
      - quantmod

    - for Prediction (support/update.R run by cron)
      - caret
        - models
          - bridge
          - ranger
          - rf
          - bagEarth
          - pls
      - doParallel
      - RSQLite
      - quantmod

- Database
  - SQLite
    - stock-explorer.sqlite3


## Target Stocks

Source of stock prices are from Yahoo Japan Finance (yahooj).

| code | name |
|------|------|
| 998407.O | 日経平均株価 |
| 3738.T | ティーガイア |
| 3774.T | インターネットイニシアティブ |
| 4689.T | ヤフー |
| 4726.T | ソフトバンク・テクノロジー |
| 4755.T | 楽天 |
| 9422.T | アイ・ティー・シーネットワーク |
| 9433.T | KDDI |
| 9434.T | ソフトバンク |
| 9435.T | 光通信 |
| 9437.T | NTTドコモ |
| 9984.T | ソフトバンクグループ |


### Note

At this moment, this application does not run properly with R/Shiny on Windows OS due to UTF-8 encoding issue.
