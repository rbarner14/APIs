# Comprehensive http library in Python.
import httplib2 
# Converts in-memory Python objects to a serialized JSON representation
import json 

def getGeocodeLocation(inputString):
    # Use Google Maps to convert a location into Latitute/Longitute coordinates
    # FORMAT: https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=API_KEY
    google_api_key = "AIzaSyD7wDmIlsJ3fCHQ_1ZKjrSEISRgNaxw6ls"
    
    # Name of the place we want to get coordinates for.
    # Replace spaces with plus signs, so that there are no breaks in URL path 
    # so that server can read it correctly.
    locationString = inputString.replace(" ", "+")
    
    # Build url and pass in location string and Google API key via Python2-type 
    # f-string formatting.
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    
    # Create instance of http class named "h".
    h = httplib2.Http()

    # Create GET request for url with request method.  
    # Request returns array with 2 values: the http response and the content.
    # Setting "result" to the value of the method json.loads called on the 
    # 2nd array: the content to format the content in a readable JSON format.
    result = json.loads(h.request(url,'GET')[1])

    # Print http response header to terminal.
    print(f'response header:{h.request(url,"GET")[0]}')

    # Return requested response: latitude & longitude.
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)

    # return result
