library(doParallel)
library(Metrics)
library(shiny)
library(shinycssloaders)
library(shinydashboard)
library(shinyEventLogger)
library(shinyjs)
library(shinyWidgets)
library(dplyr)
library(DT)
library(ggplot2)
library(RSQLite)
library(quantmod)

# =============================================================================
#
#  stock-explorer, global.R
#
# =============================================================================
# for logging
set_logging(r_console = TRUE,
            js_console = FALSE,
            "param_1" = 1,
            "param_2" = "A")

# for multi-threading
cl <- makePSOCKcluster(detectCores())
registerDoParallel(cl)

# -----------------------------------------------------------------------------
#  global variable
# -----------------------------------------------------------------------------
options("getSymbols.warning4.0" = FALSE)

# application title
app.title <- "stock-explorer"

# application version
app.ver <- "0.2"

# db start date
date.start <- "2018-12-19"

# create & connect db
dbname <- "/home/bitwalk/shiny-app/stock-explorer/stock-explorer.sqlite3"
drv <- dbDriver("SQLite")

# -----------------------------------------------------------------------------
#  common theme for ggplot2
# -----------------------------------------------------------------------------
gtheme <- theme(
  axis.title = element_text(size = 14),
  axis.text = element_text(size = 12, colour = "black"),
  axis.line = element_line(),
  legend.title =  element_text(size = 12),
  legend.text = element_text(size = 12),
  panel.grid.major = element_line(colour = "grey", size = rel(0.5)), 
  panel.grid.minor = element_blank(), 
  panel.background = element_rect(fill = "whitesmoke", colour = "black", size = 0.8)
)

# -----------------------------------------------------------------------------
#  common theme for candle chart
# -----------------------------------------------------------------------------
theme.candle <- chartTheme(
  'white',
  up.col = 'darkgreen',
  dn.col = 'orange'
)

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
#
#  FUNCTIONS
#
# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

# -----------------------------------------------------------------------------
#  as.Date.numeric - convert date number to date string
#
#  arg.
#    x: date number
#    origin: origin of date number, default value is 1970-01-01
#
#  return
#    date string
# -----------------------------------------------------------------------------
as.Date.numeric <- function(x, origin="1970-01-01", ...) {
  if ((missing(origin) && nargs()==1) || (is.character(origin) && origin=="1970-01-01" && nargs()==2))
    return(structure(as.integer(x), class="Date"))
  as.Date(origin, ...) + as.integer(x)
}

# -----------------------------------------------------------------------------
#  getCodeList
#
#  arg.
#    none
#
#  return
#    list of stock code which can be used for choices of updateSelectInput
# -----------------------------------------------------------------------------
getCodeList <- function() {
  sql <- "select * from code_list;"
  tbl <- getTblFromDB(sql)
  
  choice_list <- list()
  for (r in c(1:nrow(tbl))) {
    ticker_name <- tbl[r, "ticker_name"]
    ticker_code <- tbl[r, "ticker_code"]
    choice_list[[ticker_name]] <- ticker_code
  }

  return(choice_list)
}

# -----------------------------------------------------------------------------
#  getMethodList
#
#  arg.
#    none
#
#  return
#    list of stock code which can be used for choices of updateSelectInput
# -----------------------------------------------------------------------------
getMethodList <- function() {
  sql <- "select * from method_list;"
  tbl <- getTblFromDB(sql)

  choice_list <- list()
  for (name.method in sort(tbl$method_name)) {
    choice_list[[name.method]] <- name.method
  }
  
  return(choice_list)
}

# -----------------------------------------------------------------------------
#  getNameFromDB
#
#  arg.
#    sql : sql statement
#
#  return
#    string
# -----------------------------------------------------------------------------
getNameFromDB <- function(sql) {
  # connect db
  con <- dbConnect(drv, dbname, synchronous = NULL)
  
  # get query result
  name <- dbGetQuery(con, sql)
  
  # disconnect db
  dbDisconnect(con)
  
  return(as.character(name[1, 1]))
}

# -----------------------------------------------------------------------------
#  getPredList
#
#  arg.
#    none
#
#  return
#    list of stock code which can be used for choices of updateSelectInput
# -----------------------------------------------------------------------------
getPredList <- function() {
  sql <- "select * from code_list where flag_pred = 1;"
  tbl <- getTblFromDB(sql)
  
  choice_list <- list()
  for (r in c(1:nrow(tbl))) {
    ticker_name <- tbl[r, "ticker_name"]
    ticker_code <- tbl[r, "ticker_code"]
    choice_list[[ticker_name]] <- ticker_code
  }

  return(choice_list)
}

# -----------------------------------------------------------------------------
#  getPredTbl
#
#  arg.
#    code: ticker code
#
#  return
#    tablle includes actual & predicted open price of specified code 
# -----------------------------------------------------------------------------
getPredTbl <- function(code, name.method) {
  code.open <- paste0("YJ", code, "_Open")
  code.next <- paste0("YJ", code, "_Next")
  sql1 <- paste0("select deal_date, ", code.open, " from stock_data;")
  sql2 <- paste0("select int_date, ", code.next, " from ", name.method, ";")
  
  tbl1 <- getTblFromDB(sql1)
  tbl2 <- getTblFromDB(sql2)

  day.next <- tbl2[, 1][length(tbl2[, 1])] + 1

  tbl1 <- rbind(tbl1, c(as.character(as.Date.numeric(day.next)), NA))
  tbl1[, 1] <- as.Date(tbl1[, 1])
  
  tbl3 <- data.frame(x = as.Date.numeric(c(tbl2[, 1], day.next)), y <- c(NA, tbl2[, 2]))
  names(tbl3) <- c("deal_date", code.next)
  
  tbl <- merge(tbl1, tbl3)
  tbl[, "deal_date"] <- as.Date(tbl[, "deal_date"])
  tbl[, code.open] <- as.numeric(tbl[, code.open])
  tbl[, code.next] <- as.numeric(tbl[, code.next])
  tbl$Delta <- tbl[, code.open] - tbl[, code.next]
  
  log_output(tail(tbl))
  return(tbl)
}

# -----------------------------------------------------------------------------
#  getStartMonthDate - return first date of month with date format
#
#  arg.
#    x: date number
#
#  return
#    first date of month including x with date format
# -----------------------------------------------------------------------------
getStartMonthDate <- function(x) {
  as.Date(format(x, "%Y-%m-01"))
}

# -----------------------------------------------------------------------------
#  getStockData
#
#  arg.
#    code: ticker code
#
#  return
#    data frame including stock data for specified code
# -----------------------------------------------------------------------------
getStockData <- function(code) {
  sql <- "select * from stock_data;"
  tbl <- getTblFromDB(sql)
  
  key.date <- "deal_date"
  
  key <- gsub("\\.", "_", code)
  header <- colnames(tbl)
  col.extract <- grep(key, header)
  tbl.code <- tbl[, col.extract]
  rownames(tbl.code) <- tbl[, key.date]
  colnames(tbl.code) <- gsub("_", "\\.", colnames(tbl.code))
  
  return(tbl.code)
}

# -----------------------------------------------------------------------------
#  getTblFromDB
#
#  arg.
#    sql : sql statement
#
#  return
#    data frame as a query result
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

# -----------------------------------------------------------------------------
#  getTickerName
#
#  arg.
#    code: ticker code
#
#  return
#    string of ticker name for specified code
# -----------------------------------------------------------------------------
getTickerName <- function(code) {
  sql <- paste0("select ticker_name from code_list where ticker_code = '", code, "';")
  name <- getNameFromDB(sql)

  return(name)
}

# -----------------------------------------------------------------------------
#  getXDateGrid - create x grid for date on prediction plot
#
#  arg.
#    tbl: table used for plot including deal_date column
#
#  return
#    list of x for vertical line
# -----------------------------------------------------------------------------
getXDateGrid <- function(tbl) {
  date.first <- as.Date(tbl$deal_date[1])
  date.latest <- as.Date(tbl$deal_date[nrow(tbl)])
  date.next <- getStartMonthDate(date.first)
  
  date.list <- NULL
  while (date.next <= date.latest) {
    date.list <- c(date.list, date.next)
    date.next <- getStartMonthDate(getStartMonthDate(date.next) + 35)
  }
  
  return(date.list)
}

# -----------------------------------------------------------------------------
#  simulateInvest
#
#  arg.
#    tbl: table for prediction
#
#  return
#    data frame including simulation results
# -----------------------------------------------------------------------------
unit <- 100           # unit stock to buy/sell
principal <- 1000000  # initial cash principal
simulateInvest <- function(tbl) {
  idx.date <- grep("deal_date", colnames(tbl))
  idx.open <- grep("Open$", colnames(tbl))
  idx.pred <- grep("Next$", colnames(tbl))

  tbl.out <- data.frame(Date = tbl[, idx.date],
                        Pred = tbl[, idx.pred],
                        Open = tbl[, idx.open],
                        Flag = NA,
                        Cash = NA,
                        Own = NA,
                        Stock = NA,
                        Profit = NA,
                        Equity = NA)

  n <- c(1:nrow(tbl.out))
  price.prev <- 0
  price.bought <- 0     # price stock bought
  for (r in n) {
    price.today <- tbl.out[r, "Open"]
    if (r == 1) {
      # start
      tbl.out <- simulateInvest.start(tbl.out, r, price.today)
      #price.bought <- tbl.out[r, "Open"]
    } else {
      if ((tbl.out[r, "Pred"] > price.bought * 0.999) && (tbl.out[r - 1, "Own"] > 0)) {
        # sell
        tbl.out <- simulateInvest.sell(tbl.out, r, price.today)
      } else if (tbl.out[r - 1, "Own"] == 0) {
        # buy
        tbl.out <- simulateInvest.buy(tbl.out, r, price.today)
        if (tbl.out[r, "Flag"] == "buy"){
          price.bought <- tbl.out[r, "Open"]
        }
      } else {
        # keep
        tbl.out <- simulateInvest.keep(tbl.out, r, price.today)
      }
    }
    tbl.out[r, "Equity"] <- tbl.out[r, "Cash"] + tbl.out[r, "Stock"] + tbl.out[r, "Profit"]
    price.prev <- price.today
  }
  
  # format columns
  tbl.out$Pred <- format(round(tbl.out$Pred, 1), nsmall = 1)
  tbl.out$Open <- format(tbl.out$Open, nsmall = 1)
  tbl.out$Cash <- as.integer(tbl.out$Cash)
  tbl.out$Stock <- as.integer(tbl.out$Stock) 
  tbl.out$Profit <- as.integer(tbl.out$Profit) 
  tbl.out$Equity <- as.integer(tbl.out$Equity)

  log_output(tail(tbl.out))
  return(tbl.out)
}

# -----------------------------------------------------------------------------
#  simulateInvest.start
#
#  arg.
#    tbl:   table for simlation
#    r:     row to simulate
#    price: today's stock price
#
#  return
#    data frame including simulation results
# -----------------------------------------------------------------------------
simulateInvest.start <- function(tbl, r, price) {
  tbl[r, "Flag"] <- "start"
#  amount <- floor(principal %/% price / unit) * unit
#  if (amount > 0) {
#    tbl[r, "Own"]     <- amount
#    tbl[r, "Stock"]   <- price * tbl[r, "Own"]
#    tbl[r, "Cash"]    <- principal - tbl[r, "Stock"]
#    tbl[r, "Profit"]  <- 0
#  } else {
    tbl[r, "Own"]     <- 0
    tbl[r, "Stock"]   <- 0
    tbl[r, "Cash"]    <- principal
    tbl[r, "Profit"]  <- 0
#  }
  return(tbl)
}

# -----------------------------------------------------------------------------
#  simulateInvest.buy
#
#  arg.
#    tbl:   table for simlation
#    r:     row to simulate
#    price: today's stock price
#
#  return
#    data frame including simulation results
# -----------------------------------------------------------------------------
simulateInvest.buy <- function(tbl, r, price) {
  amount <- floor(tbl[r - 1, "Cash"] %/% price / unit) * unit

  if (is.na(amount)) {
    tbl <- simulateInvest.keep(tbl, r, price)
    return(tbl)
  }

  if (amount == 0) {
    tbl <- simulateInvest.keep(tbl, r, price)
    return(tbl)
  }

  tbl[r, "Flag"] <- "buy"
  if (!is.na(price)) {
    tbl[r, "Own"] <- tbl[r - 1, "Own"] + amount 
    tbl[r, "Stock"] <- price * tbl[r, "Own"]
    tbl[r, "Cash"] <- tbl[r - 1, "Cash"] - amount * price
    tbl[r, "Profit"] <- tbl[r - 1, "Profit"]
  } else {
    tbl[r, "Own"] <- NA 
    tbl[r, "Stock"] <- NA
    tbl[r, "Cash"] <- NA
    tbl[r, "Profit"] <- NA
  }
  return(tbl)
}

# -----------------------------------------------------------------------------
#  simulateInvest.sell
#
#  arg.
#    tbl:   table for simlation
#    r:     row to simulate
#    price: today's stock price
#
#  return
#    data frame including simulation results
# -----------------------------------------------------------------------------
simulateInvest.sell <- function(tbl, r, price) {
  amount <- tbl[r - 1, "Own"]
  if (amount == 0) {
    tbl <- simulateInvest.keep(tbl, r, price)
    return(tbl)
  }

  tbl[r, "Flag"] <- "sell"
  if (!is.na(price)) {
    cash <- tbl[r - 1, "Cash"] + amount * price
    tbl[r, "Cash"] <- principal
    tbl[r, "Profit"] <- tbl[r - 1, "Profit"] + cash - principal
    tbl[r, "Own"] <- 0
    tbl[r, "Stock"] <- 0
  } else {
    tbl[r, "Own"] <- NA 
    tbl[r, "Stock"] <- NA
    tbl[r, "Cash"] <- NA
    tbl[r, "Profit"] <- NA
  }
  return(tbl)
}

# -----------------------------------------------------------------------------
#  simulateInvest.keep
#
#  arg.
#    tbl:   table for simlation
#    r:     row to simulate
#    price: today's stock price
#
#  return
#    data frame including simulation results
# -----------------------------------------------------------------------------
simulateInvest.keep <- function(tbl, r, price) {
  tbl[r, "Flag"] <- "keep"
  if (!is.na(price)) {
    tbl[r, "Own"] <- tbl[r - 1, "Own"]
    tbl[r, "Stock"] <- tbl[r - 1, "Own"] * price
    tbl[r, "Cash"] <- tbl[r - 1, "Cash"]
    tbl[r, "Profit"] <- tbl[r - 1, "Profit"]
  } else {
    tbl[r, "Own"] <- NA 
    tbl[r, "Stock"] <- NA
    tbl[r, "Cash"] <- NA
    tbl[r, "Profit"] <- NA
  }
  return(tbl)
}
