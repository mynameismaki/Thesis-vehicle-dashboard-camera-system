import gpsd
import json
import os
import time

gpsd.connect()

while True:
    if not os.path.exists("/home/pi/Sync/GPS"):
        os.makedirs("/home/pi/Sync/GPS")
        
    try:
        packet = gpsd.get_current()
        print(packet)
        if packet.lon != 0 and packet.lat != 0:
            gps_data = {
                "latitude": packet.lat,
                "longitude": packet.lon,
                "timestamp": packet.time,
            }
            print(gps_data)

            gps_file_path = os.path.join("/home/pi/Sync/GPS", "gps_data.json")

            with open(gps_file_path, "w") as f:
                json.dump(gps_data, f)
            
        time.sleep(4)
    
    except Exception as e:
        print(e)
        time.sleep(5)
        
