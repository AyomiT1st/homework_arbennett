# Streamflow Forecasting Assignment 1

## Overview
In this assignment, you will produce a 1-week and 2-week streamflow forecast for the Verde River near Camp Verde, AZ. You'll use your existing knowledge of NumPy, Matplotlib, and pandas, along with new skills in API data retrieval, to access and analyze USGS streamflow data and DAYMET meteorological data, and perform numerical/statistical analysis to develop forecasts.

This assignnment will be due on October 7th, 2021, @ 11:59pm. As such, your forecast should be for the periods of October 7th - October 14th, and October 7th - October 21st. Forecasts should be given as a single value for each period in cubic feet per second (cfs).

## Assignment Details

This assignment is your first opportunity to build an analysis from scratch, with no starter code provided. You will need to:
- Retrieve historical streamflow and meteorological data using APIs.
- Analyze the data to identify patterns and relationships.
- Develop a streamflow forecast using one of the suggested methods.
- Create visualizations to support your analysis and forecast.
- Write a report explaining your methodology, findings, and forecast results.

### Rubric
- Data Retrieval (20%)
    -   Pulling the correct USGS and DAYMET data
    -   Data cleaning and formatting
    -   Documenting the data retrieval process & building functions
- Data Analysis (20%)
    -   Performing exploratory data analysis including basic statistics and ensuring data quality (missing values, outliers)
- Visualization (20%)
    -   Creating informative visualizations that support the analysis
    -   Using appropriate visualization types
- Forecasting Method (0%, but up to 10% extra credit)
- Report (40%)
    -  Clear explanation of methodology and findings in plain language
    -  Thoughtful discussion of forecast results
    -  Suggestions for improving the chosen forecasting method


### Data Retrieval
1. Use the USGS Water Services API to fetch historical streamflow data for the gauge **09506000**, or Verde River near Camp Verde.
2. Use the DAYMET Single Pixel Extraction API to obtain historical meteorological data (i.e. precipitation, temperature) for the same location located at **34.448, -111.789**.

### Data Analysis
1. Load the retrieved data into pandas DataFrames.
2. Perform exploratory data analysis using NumPy and pandas. Consider:
   - Calculating basic statistics (mean, median, standard deviation) for streamflow and meteorological variables
   - Identifying/plotting seasonal patterns or trends in each variable
   - Exploring correlations between meteorological variables and streamflow

### Visualization
For full credit you will need to create at least two informative visualizations using Matplotlib. Some examples include:
1. A time series plot showing historical streamflow and precipitation
2. A retrospective forecast plot showing your model's predictions compared to actual streamflow values.
3. A scatter plot or another appropriate visualization showing the relationship between a meteorological variable and streamflow, if used in your forecast

I am looking for your use of visualizations to support your analysis and provide insights into the data. Make sure to include appropriate labels, titles, and legends to make the visualizations clear and informative.

### Forecasting Methods
Choose one of the following methods to develop your 1-week and 2-week streamflow forecasts. Note that your choice in method will affect the type of analysis and reflection that I expect in your report. There is no "correct" method, but I will be looking for a thoughtful and well-reasoned reflection on your choice and its implications. If you are feeling ambitious, you can attempt the advanced method for up to 3 points extra credit.

#### 1. Persistence Forecast with Climate Consideration
- **Description**: This method assumes that future streamflow will be the same as the most recent observed streamflow.
- **Steps**:
  - a. Identify the most recent streamflow value in your dataset.
  - b. Use this value as your forecast for both 1-week and 2-week predictions.
  -  c. Analyze the past temperature and precipitation patterns:
     - Calculate the average temperature and total precipitation for the forecast periods (1 week and 2 weeks) from historical data.
     - Compare these averages to the current conditions.
  - d. Discuss how the current temperature and precipitation conditions might impact the accuracy of your persistence forecast. Consider questions like:
     - Is the current weather significantly different from the historical average?
     - How might unusually high or low temperatures affect streamflow?
     - What impact could above or below-average precipitation have on your forecast?
  - e. As a more advanced option, you could consider using trend of the last two weeks to adjust the forecast. Consider calculating trend as the difference between the last two weeks of streamflow data, and using this to adjust your forecast for the next two weeks.
  - f. Discuss the strengths and limitations of this method. Consider:
     - How well does it capture short-term variability?
     - How might it be affected by long-term trends or seasonal patterns?
     - In what situations might this method be particularly accurate or inaccurate?

#### 2. Streamflow Climatology Method
- **Description**: This method uses historical streamflow data to create a climatology (long-term average) for your forecasts.
- **Steps**:
  - a. Download the streamflow data to include only the last 30 years.
  - b. For each calendar day, calculate the average streamflow over the 30-year period by creating "climatology" with 365 (or 366) rows, each representing a day of the year and its corresponding average streamflow.
  - d. To make your forecast:
     - Identify the calendar days corresponding to your 1-week and 2-week forecast periods.
     - Look up the average streamflow for these days in your climatology DataFrame.
     - Use these averages as your forecasts.
  - e. Discuss the strengths and limitations of this method. Consider:
     - How well does it capture short-term variability?
     - How well does it capture seasonal patterns?
     - In what situations might this method be particularly accurate or inaccurate?

#### 3. Multiple Linear Regression using Temperature, Precipitation, and Streamflow (advanced)
- **Description**: This method develops a statistical relationship between historical meteorological data and streamflow to make predictions.
- **Steps**:
  - a. Prepare your data:
     - Align your streamflow, temperature, and precipitation data by date.
     - Create lagged variables (e.g., streamflow from 1 day ago, 2 days ago, etc.) as potential predictors.
     - Use historical data to create a training set (e.g., using data from 2010-2019).
  - b. Develop the regression model:
     - Use scikit-learn's LinearRegression class to create your model.
     - Consider which variables to include as predictors (e.g., lagged streamflow, recent precipitation, average temperature).
     - Fit the model on your training data.
  - c. Evaluate the model:
     - Make a figure showing the actual streamflow values and your model's predictions for the data used to fit the model.
  - d. Make your forecasts:
     - Use your model to predict streamflow for the 1-week and 2-week periods.
  - e. Discuss the strengths and limitations of this approach:
     - How well does the model capture the relationship between variables?
     - What assumptions does this method make, and when might they be violated?

### Submission Requirements
1. A Jupyter notebook containing your report, code, analysis, and visualizations.
2. A report (roughly 300-500 words, included in the jupyter notebook) explaining:
   - Your chosen forecasting method and why you selected it
   - Key findings from your data analysis
   - Your forecasting process, including any challenges encountered
   - Discussion of your forecast results and their potential accuracy
   - Suggestions for improving your chosen method
3. Your 1-week and 2-week streamflow predictions as separate values. Make sure to print these out as clearly as possible in your notebook, preferably at the end.

## Grading Criteria
- Correct implementation & use of API data retrieval (15%)
- Quality of data analysis and visualizations (25%)
- Appropriate application of chosen forecasting method (30%)
- Thoughtfulness of discussion and critical analysis (30%)

## Important Note
The focus of this assignment is on synthesizing what we have covered in class so far as well as throwing you into a real world analysis situation where you do not have all the answers. Your grade will be based on your methodology, analysis, and explanations rather than the precision of your forecast. 

Good luck, and enjoy working with real environmental data!