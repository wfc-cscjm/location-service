from LocationService import LocationService
location = LocationService(zipcode="Your Zipcode", address="Your Address", proxy=True)
print(location.getGeocode())
print(location.getInfo())