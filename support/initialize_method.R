library(RSQLite)

# =============================================================================
#  stock-explorer, support/initialize_method.R
# =============================================================================

# db name
dbname <- "/home/bitwalk/shiny-app/stock-explorer/support/stock-explorer.sqlite3"

# create & connect db
drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname, synchronous = NULL)

tblname <- "method_list"

# delete table if exists
if (dbExistsTable(con, tblname)) {
  dbRemoveTable(con, tblname)
  dbExecute(con, "vacuum;")
}

tbl.method <- data.frame(method_name = c("bridge", "ranger", "rf"))
tbl.method$method_name <- as.character(tbl.method$method_name)
dbCreateTable(con, tblname, tbl.method)
dbAppendTable(con, tblname, tbl.method)

# create index
sql <- "create index methodindex on method_list(method_name);"
dbExecute(con, sql)

# disconnect db
dbDisconnect(con)
