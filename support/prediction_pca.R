library(RSQLite)
library(caret)
library(doParallel)

# selection for modeling method
#model.method <- "bridge"
model.method <- "brnn"
#model.method <- "bagEarth"
#model.method <- "pls"
#model.method <- "ranger"
#model.method <- "rf"
#model.method <- "xgbTree"

# db name
dbname <- "/home/bitwalk/shiny-app/stock-explorer/support/stock-explorer.sqlite3"

# db start date
date.pred.start <- "2019-02-01"
int_date_start <- as.integer(as.Date(date.pred.start))

# for multi-threading
cl <- makePSOCKcluster(detectCores())
registerDoParallel(cl)

as.Date.numeric <- function(x, origin="1970-01-01", ...) {
  if ((missing(origin) && nargs()==1) || (is.character(origin) && origin=="1970-01-01" && nargs()==2))
    return(structure(as.integer(x), class="Date"))
  as.Date(origin, ...) + as.integer(x)
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
  gc()
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

# create & connect db
drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname)

sql1 <- paste0("select int_date from stock_data where int_date >= ", int_date_start, ";")
int_date_list <- dbGetQuery(con, sql1)

tbl.pred <- data.frame(int_date = int_date_list[, 1], deal_date = as.Date.numeric(int_date_list[, 1]))

#int_date <- int_date_list[, 1][nrow(int_date_list) - 1]
for (int_date in int_date_list[, 1]) {
  pred_code_list <- dbGetQuery(con, "select ticker_code from code_list where flag_pred = 1")
  
  #pred_code <-pred_code_list[, 1][1]
  for (pred_code in pred_code_list[, 1]) {
    pred_code0 <- gsub("\\.", "_", pred_code)
    pred_code_open <- paste0("YJ", pred_code0, "_Open")
    pred_code_next <- paste0("YJ", pred_code0, "_Next")
    
    # -------------------------------------------------------------------------
    # read existing stock data from db
    # -------------------------------------------------------------------------
    tbl <- dbGetQuery(con, "select * from stock_data")
    # -------------------------------------------------------------------------
    #  Principal Component Analysis, PCA
    # -------------------------------------------------------------------------
    pca <- prcomp(tbl[, grep("[^(int_date)|(deal_date)]", names(tbl))], scale = T)
    # -------------------------------------------------------------------------
    #  use PCs of whcih 'Cumulative Proportion' < 99%
    # -------------------------------------------------------------------------
    tbl_pca <- data.frame(pca$x[, summary(pca)$importance[3,] < 0.99])
    
    tbl_pca$int_date <-tbl$int_date
    tbl_pca$Y <- c(tbl[2:nrow(tbl), grep(pred_code_open, names(tbl))], NA)
    tbl.train <- tbl_pca[tbl_pca$int_date < int_date, grep("[^(int_date)]", names(tbl_pca))]
    tbl.test <- tbl_pca[tbl_pca$int_date == int_date, grep("[^(int_date)|Y]", names(tbl_pca))]
    
    int_date_list2 <- tbl[tbl$int_date > int_date, "int_date"]
    if (length(int_date_list2) > 0) {
      int_date.next <- min(int_date_list2)
      y.test.answer <- tbl[tbl$int_date == int_date.next, grep(pred_code_open, names(tbl))]
    } else {
      int_date.next <- NA
      y.test.answer <- NA
    }
    
    model <- train.model(tbl.train, model.method)
    print(model)
    
    y.pred <- predict(model, tbl.test)
    
    tbl.pred[tbl.pred$int_date == int_date, pred_code_next] <- y.pred
    result <- data.frame(Date = as.Date.numeric(int_date), Code = pred_code, Predict = y.pred, Date.Next = as.Date.numeric(int_date.next), Actual = y.test.answer)
    result$Delta <- result$Actual - result$Predict
    print(result)
  }
}

# delete table stock_data
if (dbExistsTable(con, model.method)) {
  dbRemoveTable(con, model.method)
  dbExecute(con, "vacuum;")
}

sql2 <- paste0("create table ", model.method, "(int_date INTEGER, deal_date TEXT, ")
collist <- names(tbl.pred)[3:length(names(tbl.pred))]
substr <- NULL
for (cname in collist) {
  substr <- append(substr, paste(cname, "REAL"))  
}
sql2 <- paste0(sql2, paste(substr, sep="", collapse=", "), ");")
#sql2 <- gsub("\\.", "_", sql1)
print(sql2)
dbExecute(con, sql2)

date_list <- as.character(tbl.pred$deal_date)
#date_list <- tbl.pred$deal_date
for (date_str in date_list ){
  sql3 <- paste0("insert into ", model.method, " values(", as.integer(as.Date(date_str)), ", '", date_str, "', ")
  sql3 <- paste0(sql3, paste(tbl.pred[tbl.pred$int_date == as.integer(as.Date(date_str)), collist], sep="", collapse=", "), ");")
  dbExecute(con, sql3)
  print(sql3)
}

# create index
sql4 <- paste0("create index dateindex_", model.method, " on ", model.method, "(int_date);")
dbExecute(con, sql4)

# disconnect db
dbDisconnect(con)
