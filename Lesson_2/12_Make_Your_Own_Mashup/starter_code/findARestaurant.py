from flask import Flask
from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs

# app = Flask(__name__)

# # Catchall for non-ascii characters (characters not common to the English 
# # language) render properly in code (ie. Japanese characters).
# sys.stdout = codecs.getwriter("utf8")(sys.stdout)
# sys.stderr = codecs.getwriter("utf8")(sys.stderr)

foursquare_client_id = "QVY0YIACTYI30DRWLK4ZUNT1KFQHAPGPOBKEM5DYWL0CLEJN"
foursquare_client_secret = "WRCP40LWD1NO0KUEGWINKMQNWO5HCSM4TYUDZCHUMYEMTIKP"
version = "20190425"


def findARestaurant(mealType,location):
	"""Retrieve restaraunt, address and 300x300 photo."""
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	# lat_lng = f"{getGeocodeLocation(location)}"
	# lat_lng_formatted = lat_lng[lat_lng.find("(")+1:lat_lng.find(")")]
	latitude, longitude = getGeocodeLocation(location)

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = (f"https://api.foursquare.com/v2/venues/search?client_id={foursquare_client_id}&client_secret={foursquare_client_secret}&v={version}&ll={latitude},{longitude}&intent=browse&radius=10000&query={mealType}&limit=10")
	h = httplib2.Http()
	result = json.loads(h.request(url, "GET")[1])

	#3. Grab the first restaurant
	venue_id = result["response"]["venues"][0]["id"]
	venue_name = result["response"]["venues"][0]["name"]
	venue_location = result["response"]["venues"][0]["location"]

	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	img_url = (f"https://api.foursquare.com/v2/venues/{venue_id}/photos?client_id={foursquare_client_id}&client_secret={foursquare_client_secret}&v={version}&group=venue&limit=10")
	img_h = httplib2.Http()
	img_result = json.loads(img_h.request(img_url, "GET")[1])
	print(img_result)

	#5. Grab the first image
	if len(img_result["response"]["photos"]["items"]) > 0:
		img_url = f"{img_url_pre_lim['prefix']}300x300{img_url_pre_lim['suffix']}"

	#6. If no image is available, insert default a image url
	else:
		img_url = "https://cps-static.rovicorp.com/3/JPG_400/MI0003/711/MI0003711195.jpg?partner=allrovi.com"

	#7. Return a dictionary containing the restaurant name, address, and image url	
	result = {"name": venue_name, "address": venue_location.get("address",""), "img_url": img_url}
	print(result)
	return result

################################################################################	

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")


	# app.debug = True
	# app.run(host="0.0.0.0", port=5000)




