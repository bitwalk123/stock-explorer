library(RSQLite)

# selection for modeling method
model.method <- "rf"
#model.method <- "xgbTree"

# db name
dbname <- "/home/bitwalk/shiny-app/stock-explorer/support/stock-explorer.sqlite3"
drv <- dbDriver("SQLite")

as.Date.numeric <- function(x, origin="1970-01-01", ...) {
  if ((missing(origin) && nargs()==1) || (is.character(origin) && origin=="1970-01-01" && nargs()==2))
    return(structure(as.integer(x), class="Date"))
  as.Date(origin, ...) + as.integer(x)
}

# -----------------------------------------------------------------------------
# getTblFromDB
#
# arg.
#   sql : sql statement
#
# return
#   data frame as a query result
# -----------------------------------------------------------------------------
getTblFromDB <- function(sql) {
  # connect db
  con <- dbConnect(drv, dbname, synchronous = NULL)
  
  # get query result
  tbl <- dbGetQuery(con, sql)
  
  # disconnect db
  dbDisconnect(con)
  
  return(data.frame(tbl))  
}

code <- "9434_T"
code_open <- paste0("YJ", code, "_Open")
code_next <- paste0("YJ", code, "_Next")
sql1 <- paste0("select deal_date, ", code_open, " from stock_data;")
sql2 <- paste0("select int_date, ", code_next, " from rf;")

tbl1 <- getTblFromDB(sql1)

tbl2 <- getTblFromDB(sql2)
day.next <- tbl2[, 1][length(tbl2[, 1])] + 1
tbl1 <-rbind(tbl1, c(as.character(as.Date.numeric(day.next)), NA))
tbl1[, 1] <- as.Date(tbl1[, 1])
tbl3 <- data.frame(x = as.Date.numeric(c(tbl2[, 1], day.next)), y <- c(NA, tbl2[, 2]))
names(tbl3) <- c("deal_date", code_next)

tbl <- merge(tbl1, tbl3)
