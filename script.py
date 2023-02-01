import urllib.request

from bs4 import BeautifulSoup

source = urllib.request.urlopen(
    "https://www.truckscout24.de/transporter/gebraucht/kuehl-iso-frischdienst/renault"
).read()

soup = BeautifulSoup(source, "lxml")
