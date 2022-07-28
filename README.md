# Udacity_DEND
This repo contains my projects from the Udacity Data Engineering Nano degree

# Data Engineering Capstone Project

## Project Summary

### Goal of the project
This project aims to building a data warehouse using the US immigration data set, enriching the data with the demographics of the US cities dataset and the world temperature data for data analysis. This is built for a data analytics table.

The project follows the follow steps:

- **Step 1:** Scope the Project and Gather Data
- **Step 2:** Explore and Assess the Data
- **Step 3:** Define the Data Model
- **Step 4:** Run ETL to Model the Data
- **Step 5:** Complete Project Write Up

---
## Step 1: Scope the Project and Gather Data

### Project Scope

In this project I will be integrating three data sets the immigration dataset, the temperature dataset and the US cities demographics dataset to create a data analytics table that can help answer questions like

- Immigrants move to US cities with what kind of demographics staistics?
- Immigrants move to US cities with what kind of temperature? Do they move to warmer weather or cooler weather?
- Do they move to cities with a larger population or less population?

For this project I have used [Pandas](https://pandas.pydata.org/) and [Numpy](https://numpy.org/) as tools.

Pandas has great libraries for all the exploratory Data Analysis that I wanted to do and numpy I used for analysis on certain columns. But for future I reccomend using [Spark](https://spark.apache.org/) for analysis because it allows for distributed processing and also use cloud like S3 for storage, EMR and Redshift for analysis because for larger data more processing power is needed and using CPU doesn't allow for good processing.

I have used `.py` files to create sparkifydb and tables on the localhost and I used [Jupyter](https://jupyter.org/) notebook to analyze the data and test for data quality. I used Jupyter notebook because it is easy and intuitive to use for analysis and creating the tables.

### Describe and Gather Data

#### Data Sources:

- **[I94 Immigration Data](https://www.trade.gov/national-travel-and-tourism-office):** This data comes from the US National Tourism and Trade Office. A data dictionary is included in the workspace. 
- **[World Temperature Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)**: This dataset came from Kaggle. 
- **[U.S. City Demographic Data](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/)**: This data comes from OpenSoft. 

---
## Step 2: Explore and Assess the Data

### Explore the Data
There are a few nulls in the dataset for in the immigration dataset but since the `cicid` (primary key) are not nulls leaving them as is.

### Cleaning Steps
Document steps necessary to clean the data:

- Changed SAS `timestamp` to `datetime`
- Changed certain `float` columns to `int` types
- Changed column names to more descriptive names
- For the temperature dataset only took out for Country United States since we are dealing with only US states here.
- Added country to immigration dataframe to be able to merge on the country column for analysis.
- Dropped coulmns that proved not be helpful.

---
## Step 3: Define the Data Model

### 3.1 Conceptual Data Model

The Conceptual data model is attached as a `png` file. I am using a Star Schema where:

|Fact table|Dimensional tables|
|---|---|
|`fact_immigration`|`dim_airline`|
||`dim_temperature`|
||`dim_demographics`|
||`dim_personal_info`|

When thinking about the data model, I was thinking about creating one table that has the facts on the immigration data and other table that has more details that could help answer my questions, so the Fact table for the facts and the dimension tables for the details for the analysis. 

Why I chose Star schema over snowflake schema is because:

1. Star schema is more efficient and a better way to organize the data in the dataware house;
2. Because they are superfast, simple design that I was looking for to combine my fact and dimension tables.

### 3.2 Mapping Out Data Pipelines

List the steps necessary to pipeline the data into the chosen data model.

Create the `df_immigration` table to `fact_immigration`, `df_airline` and `df_personal_info`.

From the immigration table we the Facts on the immigration, the personal info and the airline details. The temperature and the demographics table are used as it is for dimensions.

---
## Step 4: Run Pipelines to Model the Data

### 4.1 Create the data model
Build the data pipelines to create the data model. First create the `db` and tables by running python `create_tables.py` in the terminal and then running the `Capstone Project Template.ipynb` file.

### 4.2 Data Quality Checks

- Integrity constraints on the relational database on making sure the primary key is not duplicate.
- Unit tests for the scripts to ensure they are doing the right thing
- Source/Count checks to ensure completeness

## 4.3 Data dictionary

|Columns|Description|
|---|---|
|`dim_airline`|Stores information on the airline|
|`cicid`|Primary key for the i94 data|
|`airline`|Airline the passenger flew in|
|`admnum`|Admission number of the i94 immigrant|
|`fltno`|Flight number they arrived in|
|`visatype`|The type of visa that was issued|
|`dim_temperarure`|Stores details on the temperature of the US Cities|
|`dt`|Datetime when data was captured|
|`AverageTemperature`|The average temperature|
|`AverageTemperatureUncertainty`|The average Temperature Uncertainity|
|`City`|The city the data was temperatured was captured|
|`Country`|The Country is United States|


For `dim_demographics` and `dim_personal_info` table the names of the columns are self explanatory.

|Columns|Description|
|---|---|
|`fact_immigration`| Stores fact about the immigration table|
|`cicid`| The primary key for the i94 immigrant data|
|`year`| Year of the arrival of passengers|
|`month`| Month of the arrival of passengers|
|`port`| Which i94 port the immigrants arrived in|
|`arrival_date`| Arrival date|
|`departure_date`| Departure date|
|`visa`| Type of visa they arrived on|
|`mode`| Which mode: sea, air, land|
|`state_code`| Which state they arrived to|
|`Country`| Country is United States|

---
### Step 5: Complete Project Write Up

- The data was increased by 100x
- We would need to use a GPU to process data efficiently
- We would need to use more efficient tools like EMR for data analysis
- We will still use PySpark to analyze the data.
- The data populates a dashboard that must be updated on a daily basis by 7am every day.
- Use Airflow DAG to schedule daily upload to the dashboard.
- The database needed to be accessed by 100+ people. Using cloud services like AWS Redshift the data can be accessed by 100+ people.
