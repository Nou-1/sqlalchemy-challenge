
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect an existing database into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect=True)

#Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask setup
app = Flask(__name__)

#Flask routes
@app.route("/")
def welcome():
    "List all api routes"
    return ( f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start<br/>"
    f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    "Return list of precipitation and date"
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipitation_list = []
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    "Return list of stations"

    results = session.query(Station.name, Station.station).all()
    session.close()

    station_list = []
    for name, station in results:
        station_dict = {}
        station_dict['name'] = name
        station_dict['station'] = station
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    "Return list of temperature observation"

    date_one_year = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date>one_year_back).\
    order_by(Measurement.date).all()

    session.close()

    temperature_list = []
    for tobs, date in results:
        tobs_dict = {}
        tobs_dict['date'] = tobs
        tobs_dict['tobs'] = date
        temperature_list.append(tobs_dict)
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def start_route(start):
    session = Session(engine)
    trip_start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    year_ago = dt.timedelta(days=365)
    start = trip_start_date-year_ago
    end = dt.date(2017, 8, 23)
    trip_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_temp))

    session.close()
    return jsonify (trip_temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end_route(start,end):
    session = Session(engine)
    trip_start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    trip_end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    year_ago = dt.timedelta(days=365)
    start = trip_start_date - year_ago
    end = trip_end_date - year_ago
    trip_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_temp))
    session.close()

    return jsonify(trip_temp)

if __name__ == "__main__":
    app.run(debug=True)




