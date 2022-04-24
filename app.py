# Import dependencies
import datetime as dt
from secrets import token_bytes
import numpy as np 
import pandas as pd 

# Import dependencies for SQLAlchemy to access SQLite database. 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import dependencies for Flask
from flask import Flask, jsonify


# Set up the database engine for the Flask application to be able to access the SQLite db.
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database tables into classes. 
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create a variable for each of the classes to use them for reference later.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to the database.
session = Session(engine)

# Define the Flask application.
app = Flask(__name__)
# Define the welcome route (the root)
@app.route('/')
# Add the routing information for each of the other routes.
# by creating a function, and return statement will have f-strings as a 
# reference to all of the other routes.
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!<br/>
        Availabe Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs <br/>
        /api/v1.0/temp/start/end 
        ''')

# Create a separate route for the precipitation analysis for the last year. 
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create a new route for the station analysis that will return a list of all the stations.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create a new route for the monthly temperatur observations for the last year.  
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create a route for the summary statistics report.
# last route will be to report on the minimum, average, and maximum temperatures.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)