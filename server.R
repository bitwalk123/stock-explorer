# =============================================================================
#
#  stock-explorer, server.R
#
# =============================================================================
function(input, output, session) {
    set_logging_session()

    # -------------------------------------------------------------------------
    #  Stock Information
    # -------------------------------------------------------------------------
    tbl.code <- reactive(getStockData(input$code))

    # Candle Chart
    output$candle <- renderPlot({
        ticker.name <- getTickerName(input$code)
        title.chart <- paste0(ticker.name, " (", input$code, ")")
        chartSeries(
            as.xts(tbl.code()),
            type = "candlesticks",
            name = title.chart,
            theme = theme.candle
        )
    })
    
    # Stock Table
    output$price <- DT::renderDataTable(
        tbl.code(),
        options = list(dom = 'lipt', ordering = FALSE)
    )
    
    # -------------------------------------------------------------------------
    #  Prediction
    # -------------------------------------------------------------------------
    observe({
        # parsing stock code
        code <- gsub("\\.", "_", input$pred)
        # prediction table for plot
        name.method <- input$method
        tbl.pred <- getPredTbl(code, name.method)
        # trade simulation
        tbl.siml <- simulateInvest(tbl.pred)
        # basic statistics
        x.pred <- as.numeric(tbl.siml$Pred[2:(nrow(tbl.siml) - 1)])
        x.open <- as.numeric(tbl.siml$Open[2:(nrow(tbl.siml) - 1)])
        rsquare <- summary(lm(x.open ~ x.pred))$adj.r.squared
        rmse <- rmse(x.open, x.pred)
        # for equity trend
        tbl.bar <- na.omit(tbl.siml[, c("Date", "Equity")])
        tbl.bar$Equity <- tbl.bar$Equity / 1000
        
        # Prediction Chart
        output$prediction <- renderPlot({
            #par(mar=c(5, 4, 4, 2) + 0.1)
            par(mar=c(7, 4, 4, 0.5) + 0.1)
            
            idx.date <- grep("deal_date", colnames(tbl.pred))
            idx.open <- grep("Open$", colnames(tbl.pred))
            idx.pred <- grep("Next$", colnames(tbl.pred))

            y.range <- c(min(c(tbl.pred[, idx.open], tbl.pred[, idx.pred]), na.rm = TRUE),
                         max(c(tbl.pred[, idx.open], tbl.pred[, idx.pred]), na.rm = TRUE))

            plot(tbl.pred[, 1], tbl.pred[, 2],
                 main = paste0("始値 (", input$pred, ")"),
                 sub = paste0("method = ", name.method,
                              " : adj R-squared = ", format(round(rsquare, 3), nsmall = 3),
                              ", RMSE = ", format(round(rmse, 1), nsmall = 1)),
                 xlab = NA, ylab = NA, ylim = y.range,
                 las = 1, type = "n")
            
            grid(NA, NULL, lty = 2, col = "darkgray")
            grid.x <- getXDateGrid(tbl.pred)
            abline(v = grid.x, lty = 2, col = "darkgray")
            
            for (r in 2:(nrow(tbl.pred) - 1)) {
                lines(c(tbl.pred[r, idx.date], tbl.pred[r, idx.date]),
                      c(tbl.pred[r, idx.open], tbl.pred[r, idx.pred]),
                      type = "l", col = "#666666")
            }
            points(as.Date(tbl.pred[, idx.date]), tbl.pred[, idx.open], type = "l", col = "#8080FF", lty = 1)
            points(as.Date(tbl.pred[, idx.date]), tbl.pred[, idx.pred], type = "l", col = "#FF8080", lty = 1)
            points(as.Date(tbl.pred[, idx.date]), tbl.pred[, idx.open], type = "p", col = "blue", pch = 21)
            points(as.Date(tbl.pred[, idx.date]), tbl.pred[, idx.pred], type = "p", col = "red", pch = 19)
        })
        
        # equity trend
        output$equity <- renderPlot(
            ggplot(data = tbl.bar, aes(x = Date, y = Equity)) +
                geom_line(colour = "tomato", size = 0.8) + ylab("総資産（千円）") +
                gtheme
        )
        
        # simulation table
        output$pred <- DT::renderDataTable(
            tbl.siml,
            options = list(dom = 'lipt', ordering = TRUE)
        )
    })
}
