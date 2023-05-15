# Capstone Project: Financial Analysis Based on School Districts

Vanderbilt University, Master of Data Science, Capstone Project

by Hongyu Dai

# Project Overview
This project aimed to support Alliance Bernstein in their implementation of a new investment management strategy known as School District Impact, which prioritizes responsible investing to generate environmental and social impact in historically marginalized communities. Specifically, the project aimed to systematically compile key performance indicators that are essential to achieving the School District Impact mission, analyzing data over a five-year period to identify any positive or negative trends.

To study the impact of the school district on external housing prices, we selected graduation rates as our target variable. We developed useful functions to find metrics and districts based on provided IDs to help retrieve required items quickly. The data processing step involved removing NA values and checking for outliers.

The results varied greatly depending on the data and model used in the analysis. However, we found that the graduation rate has a significant impact on housing prices.

# Structure

```bash
├── TX_data
│   ├── HousePrice
│   ├── datadict
│   │   ├── district_processed
│   │   │   ├── datadict_district_year.csv
│   ├── TAPR_District
│   │   ├── TAPR_year.csv
│   │   ├── year
│   │   │   ├── report.csv
├── CA_data
│   ├── different report types
│   │   ├── sub-reports
│   │   │   ├── year
│   │   │   │   ├── num+county.csv
├── Codes
├── WebScraperDocumentation.md
├── README.md
```


# Quickstart
1. Download all packages.
    ```bash
    python3 -r install requirement.txt
    ```

2. (Optional) Obtain Texas's data.
    run `10+20_TX_WebScraper+Map.ipynb` notebook.

3. (Optional) Obtain California's data.
    ```bash
    python3 11.2_CA_webscraper.py
    ```

4. Data analyze.
    - `40_TX_DataAnalysis.ipynb`
    - `50_TX_Model.rmd`

# Data
Obtain by web crawl from scratch. Check codes for details. 

- [Web Scraper Documentation](/WebScraperDocumentation.md)
- [10+20_TX_WebScraper+Map](/10+20_TX_WebScraper+Map.ipynb)
- [11.2_CA_webscraper](/11.2_CA_webscraper.py)



# Results

Based on the analysis and findings presented, there is a strong relationship between school district quality and housing prices. The research shows that higher graduation rates and other education-related metrics are associated with higher housing prices, indicating that investing in education can have positive impacts on the housing market.

Overall, the findings of this research can be used to inform policymakers and investors in making informed decisions regarding housing and education investments, ultimately leading to positive outcomes for school district and the economy.


# Future work
- Improve pipeline to cover more functionality
- Try more models to improve its accuracy
- Further analyze the impact of Covid-19 on the housing market and explore other potential factors that may have been affected by the pandemic.
- Conduct further research to explore the relationship between graduation rates and housing prices in other regions and contexts.
- Explore other potential factors that may impact housing prices, such as diversity rates, Dropout Rate, and Extended Longitudinal Rate, and consider incorporating them into future analyses.


# Reference
1. [Texas Education Agency](https://tea.texas.gov/texas-schools)
2. [California Department of Education](https://dq.cde.ca.gov/dataquest/)
3. [House Price Data](https://www.redfin.com/news/data-center/)

# Concat

Hongyu Dai _hongyu.dai@foxmail.edu_


* Feel free to contact with any questions or if you are interested in contributing!

