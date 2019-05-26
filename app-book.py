from flask import Flask, render_template, request, jsonify 
from newmodels import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://ingvar:123@localhost/lecture4"
app.config["SQLACLHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    #Get form information.
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")
    # Make sure the flight exists.
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message="No such flight with that id.")

    # Add passenger
    flight.add_passenger(name)
    return render_template("success.html")

@app.route("/flights")
def flights():
    """ List all flights. """
    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """ List detail about a single flight. """

    # Make sure flight exists. 
    flight = Flight.query.get(flight_id)
    if flight is None: 
        return render_template("error.html", message="No such flight exists.")

    #Get all passangers
    #passengers = Passenger.query.filter_by(flight_id=flight_id).all()
    passengers = flight.passengers
    return render_template("flight.html", flight=flight, passengers=passengers)

@app.route("/api/flights/<int:flight_id>")
def flight_api(flight_id):
    """Return details about a single flight."""
    
    # Make sure flight exists. 
    flight = Flight.query.get(flight_id)
    if flight is None: 
        return jsonify({"error": "Invalid flight_id"}), 422
    
    #Get all passangers
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
            "origin": flight.origin,
            "destination": flight.destination,
            "duration": flight.duration,
            "passengers": names
    })