# sqlalchemy-challenge
Surfs Up!

## Step 1 - Climate Analysis and Exploration

Use Python and SQLAlchemy to run basic climate analysis and data exploration of a climate database. All of the following analysis is completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Use SQLAlchemy `create_engine` to connect to sqlite database.

* Use SQLAlchemy `automap_base()` to reflect tables into classes and save a reference to those classes called `Station` and `Measurement`.

* Link Python to the database by creating an SQLAlchemy session.

### Precipitation Analysis

* Find the most recent date in the data set.

* Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data.

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results using the DataFrame `plot` method.

* Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Design a query to calculate the total number of stations in the dataset.

* Design a query to find the most active stations.

  * List the stations and observation counts in descending order.

  * List which station id has the highest number of observations.

  * Using the most active station id, calculate the lowest, highest, and average temperature.

  * Using functions such as `func.min`, `func.max`, `func.avg`, and `func.count` in queries.

* Design a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filter by the station with the highest number of observations.

  * Query the last 12 months of temperature observation data for this station.

  * Plot the results as a histogram with `bins=12`.

## Step 2 - Climate App

Design a Flask API based on the developed queries developed.
