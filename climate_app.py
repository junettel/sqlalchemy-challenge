# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
max_date = list(np.ravel(latest_date))[0]
max_date = dt.datetime.strptime(max_date, '%Y-%m-%d')
max_year = int(dt.datetime.strftime(max_date, '%Y'))
max_month = int(dt.datetime.strftime(max_date, '%m'))
max_day = int(dt.datetime.strftime(max_date, '%d'))
min_date = dt.date(max_year, max_month, max_day) - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/datesearch/<start><br/>"
        f"/api/v1.0/datesearch/<start>/<end>"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp)\
                     .filter(Measurement.date >= min_date)\
                     .all()
    prcp_list = []

    for row in results:
        date_tobs_dict = {}
        date_tobs_dict["date"] = row.date
        date_tobs_dict["prcp"] = row.prcp
        prcp_list.append(date_tobs_dict)

    return jsonify(prcp_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations_list = session.query(Station.name).all()
    results = list(np.ravel(stations_list))

    return jsonify(results)

# Temperature Observation Route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    stations_activity = session.query(Measurement.station, func.count(Measurement.station))\
                               .group_by(Measurement.station)\
                               .order_by(func.count(Measurement.station).desc())\
                               .all()

    most_active_station = stations_activity[0]

    results = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
                     .filter(Measurement.date >= min_date)\
                     .filter(Measurement.station==most_active_station[0])\
                     .all()
    
    tobs_list = []

    for row in results:
        active_date_tobs_dict = {}
        active_date_tobs_dict["station"] = row.station
        active_date_tobs_dict["date"] = row.date
        active_date_tobs_dict["tobs"] = row.tobs
        tobs_list.append(active_date_tobs_dict)

    return jsonify(tobs_list)

# Start Date Route
@app.route("/api/v1.0/datesearch/<start>")
def start_only(start):
    session = Session(engine)

    tmin = func.min(Measurement.tobs)
    tavg = func.avg(Measurement.tobs)
    tmax = func.max(Measurement.tobs)
    sel = [Measurement.date, tmin, tavg, tmax]

    results = session.query(*sel)\
                     .filter(Measurement.date >= start)\
                     .group_by(Measurement.date)\
                     .order_by(Measurement.date)\
                     .all()

    date_list = []
    
    for row in results:
        date_dict = {}
        date_dict["date"] = row[0]
        date_dict["tmin"] = row[1]
        date_dict["tavg"] = row[2]
        date_dict["tmax"] = row[3]
        date_list.append(date_dict)

    return jsonify(date_list)

# Start/End Date Route
@app.route("/api/v1.0/datesearch/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    tmin = func.min(Measurement.tobs)
    tavg = func.avg(Measurement.tobs)
    tmax = func.max(Measurement.tobs)
    sel = [Measurement.date, tmin, tavg, tmax]

    results = session.query(*sel)\
                     .filter(Measurement.date >= start)\
                     .filter(Measurement.date <= end)\
                     .group_by(Measurement.date)\
                     .order_by(Measurement.date)\
                     .all()

    date_list = []
    
    for row in results:
        date_dict = {}
        date_dict["date"] = row[0]
        date_dict["tmin"] = row[1]
        date_dict["tavg"] = row[2]
        date_dict["tmax"] = row[3]
        date_list.append(date_dict)

    return jsonify(date_list)

if __name__ == '__main__':
    app.run(debug=True)