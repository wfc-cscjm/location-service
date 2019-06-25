########
# For use with Bluemix Weather API.
# Base URL, Bearer Token, and Proxy should be
# configured with envrionment variables.
########
import requests
import re
import os
import json

class LocationService:
  base_url = "https://twcservice.mybluemix.net/api/weather/v3/location"
  bearer_token = os.environ["WEATHER_SERVICE_BEARER_TOKEN"]

  def __init__(self, zipcode, address, proxy=None):
    self.zipcode = zipcode
    self.address = address
    self.index = None
    self.data = None
    self.proxy = proxy

  def setBearerToken(self, bearer_token):
    self.bearer_token = bearer_token
  
  def get(self, url):
    if self.proxy != None:
      os.environ["HTTP_PROXY"] = os.environ["PROXY"]
      os.environ["HTTPS_PROXY"] = os.environ["PROXY"]
    return requests.get(url, headers={ "Authorization": self.bearer_token })

  def getLocationData(self):
    query = "/search?query=%s&locationType=address&language=en-US" % (self.address)
    response = self.get(self.base_url + query)
    data = response.json()
    self.data = data['location']
    return data['location']

  def matchAddressWithZip(self):
    # API returns multiple address - each with a unique zip.
    # All API data is in a parallel array. Find the array index
    # of our address so that we can navigate all other data
    if (self.data == None):
      self.getLocationData()
    addresses = self.data['address']
    match = None
    for (i, address) in enumerate(addresses):
      z = re.search(r"\b%s\b" % (self.zipcode), address)
      if (z != None):
        match = { "address": address, "index": i }
        self.index = match['index']
        break
    return match

  def getGeocode(self):
    if (self.index == None):
      self.matchAddressWithZip()
    latitudes = self.data['latitude']
    longitudes = self.data['longitude']
    return {
      "latitude": latitudes[self.index],
      "longitude": longitudes[self.index]  
    }
  
  def getInfo(self):
    if (self.index == None):
      self.matchAddressWithZip()
    information = {}
    for key in self.data:
      information[key] = self.data[key][self.index]
    return information
