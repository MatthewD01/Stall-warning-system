import xpc
import time
import csv
from itertools import zip_longest


class XPlane:

    def __init__(self):
        self.client = xpc.XPlaneConnect()
            

    def getData(self):

        data_refs = {
            "AoA" : [],
            "Pitch" : [],
            "Flight path" : [], 
<<<<<<< HEAD
            "Velocity" : [],
=======
>>>>>>> 3898f46860863ee487a88b22f2c532b1fb51f5e9
            "Time" : []
        }
        
        
        AoA = self.client.getDREF("sim/flightmodel2/misc/AoA_angle_degrees")
        pitch = self.client.getDREF("sim/flightmodel/position/theta")
<<<<<<< HEAD
        flight_path = self.client.getDREF("sim/flightmodel/position/hpath")
        velocity = self.client.getDREF("sim/flightmodel/forces/vz_air_on_acf")
=======
        flight_path = self.client.getDREF("sim/flightmodel/position/")
>>>>>>> 3898f46860863ee487a88b22f2c532b1fb51f5e9
        time = self.client.getDREF("sim/cockpit2/clock_timer/elapsed_time_seconds")
            
        data_refs["AoA"].append(AoA)
        data_refs["Flight path"].append(pitch)
        data_refs["Pitch"].append(flight_path)
<<<<<<< HEAD
        data_refs["Velocity"].append(velocity)
=======
>>>>>>> 3898f46860863ee487a88b22f2c532b1fb51f5e9
        data_refs["Time"].append(time)
        print(data_refs)
        
    def writeData(data_refs):
        with open('data.csv', 'w', newline='') as file:
        
          writer = csv.writer(file)
          writer.writerow(data_refs.keys())
          rows = list(zip_longest(*data_refs.values()))
          writer.writerows(rows)
        
    
if __name__ == "__main__":
        client = XPlane()
        while True:
            try:
                all_data = client.getData()
                time.sleep(0.5)
            except TimeoutError:
                print("Connection stopped")
        
        # client.writeData(all_data)
        
    


