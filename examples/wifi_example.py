import tinkerlib.wifi
import urequests

# Connect to wifi
tinkerlib.wifi.connect("DIKU2", "PeterNaur")

# Do a simply GET
response = urequests.get("https://loripsum.net/api")
print(response.text)
