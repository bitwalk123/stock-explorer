library(RSQLite)
library(quantmod)

# =============================================================================
#  stock-explorer, support/initialize_db.R
# =============================================================================
options("getSymbols.warning4.0" = FALSE)

# db name
dbname <- "/home/bitwalk/shiny-app/stock-explorer/support/stock-explorer.sqlite3"
# always create new db
if (file.exists(dbname)) file.remove(dbname)

# db start date
date.start <- "2018-12-19"

# create & connect db
drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname, synchronous = NULL)

as.Date.numeric <- function(x, origin="1970-01-01", ...) {
  if ((missing(origin) && nargs()==1) || (is.character(origin) && origin=="1970-01-01" && nargs()==2))
    return(structure(as.integer(x), class="Date"))
  as.Date(origin, ...) + as.integer(x)
}

# -----------------------------------------------------------------------------
# code_list table
# -----------------------------------------------------------------------------
dbExecute(con, "create table code_list(ticker_code TEXT, ticker_name TEXT, flag_pred INTEGER)")
dbExecute(con, "insert into code_list values('998407.O', '日経平均株価',                   0);")
dbExecute(con, "insert into code_list values('3738.T',   'ティーガイア',                   1);")
dbExecute(con, "insert into code_list values('3774.T',   'インターネットイニシアティブ',   1);")
dbExecute(con, "insert into code_list values('4689.T',   'ヤフー',                         1);")
dbExecute(con, "insert into code_list values('4726.T',   'ソフトバンク・テクノロジー',     1);")
dbExecute(con, "insert into code_list values('4755.T',   '楽天',                           1);")
dbExecute(con, "insert into code_list values('9422.T',   'アイ・ティー・シーネットワーク', 1);")
dbExecute(con, "insert into code_list values('9433.T',   'KDDI',                           1);")
dbExecute(con, "insert into code_list values('9434.T',   'ソフトバンク',                   1);")
dbExecute(con, "insert into code_list values('9435.T',   '光通信',                         1);")
dbExecute(con, "insert into code_list values('9437.T',   'NTTドコモ',                      1);")
dbExecute(con, "insert into code_list values('9984.T',   'ソフトバンクグループ',           1);")

# -----------------------------------------------------------------------------
# stock_data table
# -----------------------------------------------------------------------------
code_list <- dbGetQuery(con, "select ticker_code from code_list")
tbl <- data.frame()
for (code in code_list$ticker_code) {
  if (length(grep("\\.X$", code)) > 0) {
    code <- gsub("\\.", "=", code)
  }
  print(code)
  if (nrow(tbl) > 0) {
    tbl <- merge(tbl, getSymbols(code, src = "yahooj", from = date.start, auto.assign = FALSE))
    
  } else {
    tbl <- getSymbols(code, src = "yahooj", from = date.start, auto.assign = FALSE)
  }
}
tbl <- na.omit(data.frame(tbl))
#tbl <- tbl[apply(tbl, 1, fun ction(r){!any(is.na(r))}), ]
print(tail(tbl))

sql1 <- "create table stock_data(int_date INTEGER, deal_date TEXT, "
substr <- NULL
for (cname in colnames(tbl)) {
  substr <- append(substr, paste(cname, "REAL"))  
}
sql1 <- paste0(sql1, paste(substr, sep="", collapse=", "), ");")
sql1 <- gsub("\\.", "_", sql1)
print(sql1)
dbExecute(con, sql1)

date_list <- rownames(tbl)
for (date_str in date_list ){
  sql2 <- paste0("insert into stock_data values(", as.integer(as.Date(date_str)), ", '", date_str, "', ")
  sql2 <- paste0(sql2, paste(tbl[date_str,], sep="", collapse=", "), ");")
  dbExecute(con, sql2)
}

# create index
sql3 <- "create index dateindex on stock_data(int_date);"
dbExecute(con, sql3)

# disconnect db
dbDisconnect(con)
