# =============================================================================
#
#  stock-explorer, ui.R
#
# =============================================================================

# preparing code list for selectInput with inputId = code
codeList <- getCodeList()

# preparing prediction code list for selectInput with inputId = pred
predList <- getPredList()

# preparing method list for selectInput with inputId = method
methodList <- getMethodList()

# -----------------------------------------------------------------------------
#  dashboard
# -----------------------------------------------------------------------------
dashboardPage(
    dashboardHeader(
        title = paste(app.title, app.ver)
    ),
    dashboardSidebar(
        collapsed = TRUE,
        sidebarMenu(
            menuItem(
                "株価",
                icon = icon("line-chart"),
                tabName = "tab_Stock"
            ),
            menuItem(
                "予測",
                icon = icon("calculator"),
                tabName = "tab_Pred"
            )
        )
    ),
    dashboardBody(
        includeScript(path = "myscript.js"),
        shinyjs::useShinyjs(),
        tags$head(
            tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
        ),
        tabItems(
            # -----------------------------------------------------------------
            #  Candle Chart
            # -----------------------------------------------------------------
            tabItem(
                tabName = "tab_Stock",
                width = 12,
                # selector for stock code
                selectInput(
                    inputId = "code",
                    label = NULL,
                    choices = codeList
                ),
                # candle chart
                plotOutput("candle") %>% withSpinner(),
                hr(),
                # stock data
                DT::dataTableOutput("price")
            ),
            # -----------------------------------------------------------------
            #  Prediction
            # -----------------------------------------------------------------
            tabItem(
                tabName = "tab_Pred",
                fluidPage(
                    width = 12,
                    # selector for stock code
                    selectInput(
                        inputId = "pred",
                        label = NULL,
                        choices = predList,
                    ),
                    # selector for method of ML
                    selectInput(
                        inputId = "method",
                        label = NULL,
                        choices = methodList
                    ),
                    fluidRow(
                        # prediction chart
                        plotOutput("prediction") %>% withSpinner()
                    ),
                    fluidRow(
                        plotOutput("equity", height = "150px")
                    ),
                    fluidRow(
                        # prediction data
                        DT::dataTableOutput("pred")
                    )
                )
            )
        )
    )
)
