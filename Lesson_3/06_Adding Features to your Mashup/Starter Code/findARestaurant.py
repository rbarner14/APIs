# -*- coding: utf-8 -*-
import json 
import httplib2 # Imported to make HTTP requests.

# Imported to enable non-ascii characters (non-English language) to render 
# properly in code.
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# API Keys
foursquare_client_id = 'QVY0YIACTYI30DRWLK4ZUNT1KFQHAPGPOBKEM5DYWL0CLEJN'
foursquare_client_secret = 'WRCP40LWD1NO0KUEGWINKMQNWO5HCSM4TYUDZCHUMYEMTIKP'
google_api_key = 'AIzaSyBKoTTTlfbbk0wKLFISgiJx_4jCYOdLwZs'

# Geocode location (return coordinates of a location) by passing in search 
# string and creating a Google API GET request.
def getGeocodeLocation(inputString):
    #Replace spaces in argument passed in as search string with '+' in URL.
    locationString = inputString.replace(" ", "+")
    # Google URL (Uniform Resource Locator); web address, web resource.
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    
    # Create Http Class instance and name this object 'h'. 
    h = httplib2.Http()
    # h.request(url,'GET') is a get request on the URL passed in.  The response
    # is a list of 2 items: the first, the status code & message, the 2nd, is
    # the requested info.  This is then jsonified with the loads method imported
    # from the json library and stored as the variable "result".
    result = json.loads(h.request(url,'GET')[1])

    # The json result is parsed for the data we need: lat & lng.
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    
    # Latitude and longitude are returned as a tuple.
    return (latitude,longitude) 

# This function takes in a string representation of a location and cuisine type, 
# geocodes the location, and then passes in the latitude and longitude 
# coordinates to a string that becomes the Foursquare API GET request.
def findARestaurant(mealType, location):

    # Parse tuple resulting from the return value of the getGeocodeLocation
    # function with the location of search passed into it called.  Bind 
    # latitude to the first item in tuple and longitude to the 2nd.
    latitude, longitude = getGeocodeLocation(location)
    # Create URL with latitude, longitude, API keys and meal type.
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])

    # Return restaraunt info diction if a restaraunt that matches search exists;
    # return "No Restaraunts Found" otherwise.
    if result['response']['venues']:
        # Grab the first restaurant, its id, name and address.
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id'] 
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        # Format the Restaurant Address into one string.
        address = ""

        for i in restaurant_address:
            address += i + " "

        restaurant_address = address
        
        # Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
        result = json.loads(h.request(url,'GET')[1])
        
        # Grab the first image.
        # If no image available, insert default image url.
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

        restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
        #print "Restaurant Name: %s " % restaurantInfo['name']
        #print "Restaurant Address: %s " % restaurantInfo['address']
        #print "Image: %s \n " % restaurantInfo['image']
        print(restaurantInfo)
        return restaurantInfo
    else:
        #print "No Restaurants Found for %s" % location
        return "No Restaurants Found"


################################################################################
# Enable running at command line.
if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland") 
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Austrailia")
