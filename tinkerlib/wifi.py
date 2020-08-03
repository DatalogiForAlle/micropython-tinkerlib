import time
import network


# Connect to a specific wifi network
def connect(essid, password, timeout=30000):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("Connecting to WiFi network...")
        wifi.connect(essid, password)
        # Wait until connected
        t = time.ticks_ms()
        while not wifi.isconnected():
            if time.ticks_diff(time.ticks_ms(), t) > timeout:
                wifi.disconnect()
                print("Timeout. Could not connect.")
                return False
        print("Successfully connected to " + essid)
        return True
    else:
        print("Already connected")
        return True


def disconnect():
    wifi = network.WLAN(network.STA_IF)
    wifi.disconnect()


def isconnected():
    wifi = network.WLAN(network.STA_IF)
    return wifi.isconnected()


def ipaddress():
    wifi = network.WLAN(network.STA_IF)
    ip, subnetmask, gateway, dns = wifi.ifconfig()
    return ip
