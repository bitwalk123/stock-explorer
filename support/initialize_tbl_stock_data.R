library(RSQLite)
library(quantmod)

# =============================================================================
# stock-explorer, support/initialize_tbl_stock_data.R
# =============================================================================
options("getSymbols.warning4.0" = FALSE)

# db name
dbname <- "/home/bitwalk/shiny-app/stock-explorer/support/stock-explorer.sqlite3"

# db start date
date.start <- "2018-12-19"

# create & connect db
drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname)

as.Date.numeric <- function(x, origin="1970-01-01", ...) {
  if ((missing(origin) && nargs()==1) || (is.character(origin) && origin=="1970-01-01" && nargs()==2))
    return(structure(as.integer(x), class="Date"))
  as.Date(origin, ...) + as.integer(x)
}

# -----------------------------------------------------------------------------
# stock_data table
# -----------------------------------------------------------------------------
tblname <- "stock_data"

# delete table stock_data
if (dbExistsTable(con, tblname)) {
  dbRemoveTable(con, tblname)
  dbExecute(con, "vacuum;")
}

# obtain list of ticker code from code_list table
code_list <- dbGetQuery(con, "select ticker_code from code_list;")
# obtain stock data from internet
tbl <- data.frame()
for (code in code_list$ticker_code) {
  print(code)
  if (nrow(tbl) > 0) {
    tbl <- merge(tbl, getSymbols(code, src = "yahooj", from = date.start, auto.assign = FALSE))
  } else {
    tbl <- getSymbols(code, src = "yahooj", from = date.start, auto.assign = FALSE)
  }
}
tbl <- data.frame(tbl)
print(tail(tbl))

sql1 <- paste0("create table ", tblname, "(int_date INTEGER, deal_date TEXT, ")
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
  sql2 <- paste0("insert into ", tblname, " values(", as.integer(as.Date(date_str)), ", '", date_str, "', ")
  sql2 <- paste0(sql2, paste(tbl[date_str,], sep="", collapse=", "), ");")
  dbExecute(con, sql2)
}

# create index
sql3 <- paste0("create index dateindex on ", tblname, "(int_date);")
dbExecute(con, sql3)

# disconnect db
dbDisconnect(con)
