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
        f"/api/v1.0/<start>(YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>(YYYY-MM-DD)/<end>(YYYY-MM-DD)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = list(np.ravel(max_date))[0]
    min_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.tobs)\
                     .filter(Measurement.date >= min_date)\
                     .group_by(Measurement.date)\
                     .all()

    prcp_data = []
    for row in results:
        date_tobs_dict = {}
        date_tobs_dict["date"] = row.date
        date_tobs_dict["tobs"] = row.tobs
        prcp_data.append(date_tobs_dict)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.name).all()

# @app.route("/api/v1.0/tobs")
# def robs():
#     session = Session(engine)
#     results = session.query(Measurement.tobs)
# @app.route("/api/v1.0/<start>(YYYY-MM-DD)")
# @app.route("/api/v1.0/<start>(YYYY-MM-DD)/<end>(YYYY-MM-DD)")

if __name__ == '__main__':
    app.run(debug=True)