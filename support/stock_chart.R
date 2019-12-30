library(RSQLite)
library(quantmod)

# =============================================================================
# stock-explorer, support/stock_chart.R
# =============================================================================
options("getSymbols.warning4.0" = FALSE)

# db name
dbname <- "/home/bitwalk/shiny-app/stock-explorer/support/stock-explorer.sqlite3"

# create & connect db
drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname, synchronous = NULL)
tbl <- dbGetQuery(con, "select * from stock_data")

# disconnect db
dbDisconnect(con)

key.date <- "deal_date"
ticker.code <- '9434.T'

key <- gsub("\\.", "_", ticker.code)
header <- colnames(tbl)
col.extract <- grep(key, header)
tbl.code <- tbl[, col.extract]
rownames(tbl.code) <- tbl[, key.date]
colnames(tbl.code) <- gsub("_", "\\.", colnames(tbl.code))

# candle chart
chartSeries(
  as.xts(tbl.code),
  type = "candlesticks",
  name = code,
  theme = chartTheme('white', up.col = 'darkgreen', dn.col = 'orange')
)
