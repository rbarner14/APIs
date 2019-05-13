# Imported from findARestaurant.py to find restaraunt data to populate our 
# database with.
from findARestaurant import findARestaurant 
# Database object classes Base and Restaraunt from models.py are used to fulfill
# client requests.
from models import Base, Restaurant

# Imported to instantiate app (Flask), jsonify results to make them readible by
# front end (jsnoify), and get and update data from database/to endpoints.
from flask import Flask, jsonify, request

# Imported to complete queries of database and establish relationships between 
# tables in database.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


# API Keys
foursquare_client_id = 'QVY0YIACTYI30DRWLK4ZUNT1KFQHAPGPOBKEM5DYWL0CLEJN'
foursquare_client_secret = 'WRCP40LWD1NO0KUEGWINKMQNWO5HCSM4TYUDZCHUMYEMTIKP'
google_api_key = 'AIzaSyBKoTTTlfbbk0wKLFISgiJx_4jCYOdLwZs'

# Create engine by referencing SQLite database restaraunts.db created with 
# models.py.  Alternative: PostgreSQL.
engine = create_engine('sqlite:///restaurants.db') 

# Prepare database for use in app (connect to app).
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# Imported for SQLAlchemy queries and requests.
session = DBSession() 
# Instantiate Flask app.
app = Flask(__name__)

# App decorator to set up restaraunt route that accepts 'GET' (show) and 'POST'
# (update) method requests.
@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    # Return all restaraunts in database.
    # If request method is GET, run a query on the database's Restaraunt table
    # (Class) for all restaraunts. Return value is a list of Restaurant objects.
    if request.method == 'GET':
        restaraunts = session.query(Restaurant).all()
        print(restaurants)

        # Query results (variable restaraunts which is a list data type) are 
        # serialized, or, made into a dictionary then added to a list via a list 
        # comprehension.  This list is then jsonfied for injestion by front end.
        return jsonify(restaurants = [i.serialize for i in restaraunts])

    # Make a new restaraunt and store it in the database.
    elif request.method == 'POST':
        # Flask.Request.args creates a MultiDict (dictionary subclass customized
        # to deal with multiple values for the same key which, is used by the 
        # parsing functions in the wrappers. This is necessary because some HTML 
        # form elements pass multiple values for the same key.) with the parsed 
        # contents of the query string (strings in the URL after the "?").
        # Prototype: get(key, default=None, type=None)
        location = request.args.get('location', '') 
        mealType = request.args.get('mealType', '')

        # Create restaraunt_info variable by calling the imported 
        # findARestaurant function.
        restaurant_info = findARestaurant(mealType, location)

        # If there is restaraunt info, create a restaurant variable that is 
        # equal to the instantiation of the Restaurant Class defined in our 
        # model(models.py).
        if restaurant_info != "No Restaurants Found":
            restaurant = Restaurant(restaurant_name=unicode(restaurant_info['name']),
                                    restaurant_address=unicode(restaurant_info['address']),
                                    restaurant_image = restaurant_info['image'])
            # Add restaraunt variable just created to session.
            session.add(restaurant) 
            # Commit Restaurant instance (restaurant variable created) to db.
            session.commit()

            # Return jsonified dictionary that results when object is serialized
            # via the Restaurant serialize attribute method.
            return jsonify(restaurant=restaurant.serialize)
        else:
            # If no restaurant data resulted from running findARestaurant on 
            # the meal type and location passed in the address bar upon url 
            # request, return error message.
            return jsonify({"error":f"No Restaurants Found for {mealType} in {location}"})

# Delete is in red to emphasize impact.
@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaraunt_handler(id):
    # Return restaurant database query result as a string, not list, since we
    # are querying for a line item by a specific id and the ids in our database
    # are unique.
    restaurant = session.query(Restaurant).filter_by(id=id).one()

    if request.method == 'GET':
        # Return a specific restaurant.
        return jsonify(restaurant=restaurant.serialize)
    elif request.method == 'PUT':
        # Update a specific restaurant.
        # Method request.args.get is not passed a 2nd parameter of an empty
        # string since we know forsure the restaurant object being requested is 
        # in the database and has an address (actual or empty string) as we are 
        # only updating the lineitem in the database (PUT request).
        address = request.args.get('address') 
        image = request.args.get('image')
        name = request.args.get('name')

        if address:
            restaurant.restaurant_address = address
        if image:
            restaurant.restaurant_image = image
        if name:
            restaurant.restaurant_name = name
        # Always commit action to database when manipulating it in someway
        # ('PUT', 'POST', 'DELETE')
        session.commit()

        # Jsonify the result of the restaurant variable that is serialized after
        # applying the serialize method attribute on it. 
        return jsonify(restaurant=restaurant.serialize)

    elif request.method == 'DELETE':
        # Delete a specific restaurant.

        # Delete object instance and commit action to session.
        session.delete(restaurant)
        session.commit()

        # Return message for DevX purposes.
        return "Restaurant Deleted"


################################################################################
# To run app at command line.  Debug mode is on.  Web local host # is 0.0.0.0
# and the port to run app on is 5000.
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
