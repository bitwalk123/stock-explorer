library(caret)
library(doParallel)
library(RSQLite)
library(quantmod)

# =============================================================================
#
#  stock-explorer, support/update.R
#
# =============================================================================
options("getSymbols.warning4.0" = FALSE)

# for multi-threading
cl <- makePSOCKcluster(detectCores())
registerDoParallel(cl)

# db name
#dbname <- "/home/bitwalk/shiny-app/stock-explorer/support/stock-explorer.sqlite3"
dbname <- "/home/bitwalk/shiny-app/stock-explorer/stock-explorer.sqlite3"

# db start date
date.start <- "2018-12-19"

# -----------------------------------------------------------------------------
# as.Date.numeric
# -----------------------------------------------------------------------------
as.Date.numeric <- function(x, origin="1970-01-01", ...) {
  if ((missing(origin) && nargs()==1) || (is.character(origin) && origin=="1970-01-01" && nargs()==2))
    return(structure(as.integer(x), class="Date"))
  as.Date(origin, ...) + as.integer(x)
}

# -----------------------------------------------------------------------------
#  getUpdatedStockTbl
#  get stock value from Yahoo stock site
#
#  tbl:       data frame to store stock data
#  code_list: stock code list to obtain
#
#  return
#    data frame containing stock values after eliminating rows contains NA
# -----------------------------------------------------------------------------
getUpdatedStockTbl <- function(tbl, code_list) {
  for (code in code_list$ticker_code) {
    if (length(grep("\\.X$", code)) > 0) {
      code <- gsub("\\.", "=", code)
    }
    if (code == "998407.O") {
      code = "^N225"
    }
    print(paste(code, date.latest))
    tryCatch(
      tmp <- getSymbols(code, src = "yahoo", from = date.latest, auto.assign = FALSE),
      error = function(e) {
        tmp <- data.frame()
        names(tmp) <- names(tbl)
      }      
    )
    if (exists("tmp")) {
      if (nrow(tbl) > 0) {
        tbl <- merge(tbl, tmp)
      } else {
        tbl <- tmp[, 1:4]
      }
    }
  }
  
  return(tbl)
}

# -----------------------------------------------------------------------------
#  Function: train.model
#  train model with specified ML method
#
#  df:          data frame for training including Y column
#  name.method: ML method
#
#  return
#    trained model
# -----------------------------------------------------------------------------
train.model <- function(df, name.method) {
  gc(verbose = FALSE, full = TRUE)
  set.seed(0)
  model <- train(
    Y ~ ., 
    data = df, 
    method = name.method, 
    tuneLength = 10,
    preProcess = c('center', 'scale'),
    trControl = trainControl(method = "cv")
  )
  return(model)
}

# -----------------------------------------------------------------------------
#  MAIN
# -----------------------------------------------------------------------------

# connect db
drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname)

# code list
code_list <- dbGetQuery(con, "select ticker_code from code_list")

# latest date in data base
date.latest <- as.Date.numeric(as.integer(dbGetQuery(con, "select max(int_date) from stock_data"))) 

# get stock data
tbl <- data.frame()
tbl <- getUpdatedStockTbl(tbl, code_list) 
tbl <- na.omit(data.frame(tbl))

if (nrow(tbl) > 0) {
  # update stock_data
  date_list <- rownames(tbl)
  for (date_str in date_list ){
    if (as.Date(date_str) > date.latest) {
      sql1 <- paste0("insert into stock_data values(", as.integer(as.Date(date_str)), ", '", date_str, "', ")
      sql1 <- paste0(sql1, paste(tbl[date_str,], sep = "", collapse = ", "), ");")
      print(sql1)
      dbExecute(con, sql1)
    }
  }
  
  # modeling method
  list.method <- data.frame(dbGetQuery(con, "select method_name from method_list"))
  
  # predction
  for (model.method in sort(list.method$method_name)) {
    print(model.method)
    sql2 <- paste0("select int_date from stock_data where int_date > ", as.integer(as.Date(date.latest)), ";")
    print(sql2)
    int_date_list <- dbGetQuery(con, sql2)
    tbl.pred <- data.frame(int_date = int_date_list[, 1], deal_date = as.Date.numeric(int_date_list[, 1]))
    
    for (int_date in int_date_list[, 1]) {
      pred_code_list <- dbGetQuery(con, "select ticker_code from code_list where flag_pred = 1")
      
      for (pred_code in pred_code_list[, 1]) {
        pred_code0 <- gsub("\\.", "_", pred_code)
        pred_code_open <- paste0("YJ", pred_code0, "_Open")
        pred_code_next <- paste0("YJ", pred_code0, "_Next")
        
        # -----------------------------------------------------------------------
        # read existing stock data from db
        # -----------------------------------------------------------------------
        tbl <- dbGetQuery(con, "select * from stock_data")
        # -----------------------------------------------------------------------
        #  Principal Component Analysis, PCA
        # -----------------------------------------------------------------------
        pca <- prcomp(tbl[, grep("[^(int_date)|(deal_date)]", names(tbl))], scale = T)
        # -----------------------------------------------------------------------
        #  use PCs of whcih 'Cumulative Proportion' < 99%
        # -----------------------------------------------------------------------
        tbl_pca <- data.frame(pca$x[, summary(pca)$importance[3,] < 0.99])
        
        tbl_pca$int_date <-tbl$int_date
        tbl_pca$Y <- c(tbl[2:nrow(tbl), grep(pred_code_open, names(tbl))], NA)
        tbl.train <- tbl_pca[tbl_pca$int_date < int_date, grep("[^(int_date)]", names(tbl_pca))]
        tbl.test <- tbl_pca[tbl_pca$int_date == int_date, grep("[^(int_date)|Y]", names(tbl_pca))]
        
        model <- train.model(tbl.train, model.method)
        print(model)
        
        y.pred <- predict(model, tbl.test)
        
        tbl.pred[tbl.pred$int_date == int_date, pred_code_next] <- y.pred
        result <- data.frame(Date = as.Date.numeric(int_date), Code = pred_code, Predict = y.pred)
        print(result)
      }
    }
    
    # update predictions to database
    tbl2 <- tbl.pred[, !(colnames(tbl.pred) %in% c("int_date", "deal_date"))]
    date_list <- rownames(tbl2) <- tbl.pred$deal_date
    for (date_str in date_list ){
      sql3 <- paste0("insert into ", model.method, " values(", as.integer(as.Date(date_str)), ", '", as.character(as.Date(date_str)), "', ")
      sql3 <- paste0(sql3, paste(tbl2[as.character(as.Date(date_str)),], sep = "", collapse = ", "), ");")
      print(sql3)
      dbExecute(con, sql3)
    }
  }
} else {
  print("Sorry, there is no data to update!")
}

# disconnect db
dbDisconnect(con)
