import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

fact_immigration_table_drop = "DROP TABLE IF EXISTS fact_immigration;"
dim_airline_table_drop = "DROP TABLE IF EXISTS dim_airline;"
dim_temperature_table_drop = "DROP TABLE IF EXISTS dim_temperature;"
dim_demographics_table_drop = "DROP TABLE IF EXISTS dim_demographics;"
dim_personal_info_table_drop = "DROP TABLE IF EXISTS dim_personal_info;"

# CREATE TABLES

fact_immigration_table_create= ("""
CREATE TABLE IF NOT EXISTS fact_immigration (
        cicid             float PRIMARY KEY,
        year              integer,
        month             integer,
        port              varchar,
        arrival_date      timestamp,
        departure_date    timestamp,
        visa              numeric,
        mode              float,
        state_code        varchar,
        Country           varchar
    );
""")

dim_airline_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_airline (
        cicid             float PRIMARY KEY,
        airline           varchar,
        admnum            float,
        fltno             varchar,
        visatype          varchar
    );
""")

dim_temperature_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_temperature (
        dt                                       varchar,
        AverageTemperature                       float,
        AverageTemperatureUncertainty            float,
        City                                     varchar,
        Country                                  varchar
        
    );
""")

dim_demographics_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_demographics (
        City                       varchar,
        State                      varchar,
        median_age                float,
        male_population           float,
        female_population         float,
        total_population            integer,
        no_of_veterans            float,
        foreign_born              float,
        household_size            float,
        state_code                varchar,
        Race                       varchar,
        Count                       integer
    );
""")

dim_personal_info_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_personal_info (
        cicid             float PRIMARY KEY,
        citizenship       float,
        residency         float,
        state_code        varchar,
        age               integer,
        gender             varchar,
        insnum             varchar,
        birth_year         integer,
        occupation         varchar,
        admission_date     varchar
       );
""")


# FINAL TABLES

fact_immigration_table_insert= ("""
    INSERT INTO fact_immigration (cicid, year, month, port, arrival_date, departure_date,visa, mode, state_code, Country) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
""")

dim_airline_table_insert = ("""
    INSERT INTO dim_airline (cicid, airline, admnum, fltno, visatype) 
    VALUES (%s, %s, %s, %s, %s);
""")

dim_temperature_table_insert = ("""
INSERT INTO dim_temperature (dt, AverageTemperature, AverageTemperatureUncertainty, City, Country) 
    VALUES (%s, %s, %s, %s, %s);
""")

dim_demographics_table_insert = ("""
INSERT INTO dim_demographics (City, State, median_age, male_population, female_population, total_population,no_of_veterans, foreign_born, household_size, state_code, Race, Count) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
""")

dim_personal_info_table_insert = ("""
INSERT INTO dim_personal_info (cicid, citizenship, residency, state_code, age, gender, insnum, birth_year, occupation, admission_date) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
""")


# QUERY LISTS

create_table_queries = [fact_immigration_table_create, dim_airline_table_create , dim_temperature_table_create, dim_demographics_table_create, dim_personal_info_table_create]
drop_table_queries = [fact_immigration_table_drop, dim_airline_table_drop, dim_temperature_table_drop, dim_demographics_table_drop, dim_personal_info_table_drop]
insert_table_queries = [fact_immigration_table_insert, dim_airline_table_insert, dim_temperature_table_insert, dim_demographics_table_insert, dim_personal_info_table_insert]
