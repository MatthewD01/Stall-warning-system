import xpc
import time
import csv
import pandas

class XPlane:

    def __init__(self):
        self.client = xpc.XPlaneConnect()
            

    def getData(self):

        data_refs = {
            "AoA" : [],
            "Pitch" : [],
            "Flight path" : [], 
            "Time" : []
        }
        
        
        AoA = self.client.getDREF("sim/flightmodel2/misc/AoA_angle_degrees")
        pitch = self.client.getDREF("sim/flightmodel/position/theta")
        flight_path = self.client.getDREF("sim/flightmodel/position/")
        time = self.client.getDREF("sim/cockpit2/clock_timer/elapsed_time_seconds")
            
        data_refs["AoA"].append(AoA)
        data_refs["Flight path"].append(pitch)
        data_refs["Pitch"].append(flight_path)
        data_refs["Time"].append(time)
        print(data_refs)
        
    def writeData(data_refs):
        df = open("datarefs.txt", "a")
        writing = csv.DictWriter(file, data_refs.keys())
        writing.writeheader()
        writing.writerow(data_refs)
        
    
if __name__ == "__main__":
        client = XPlane()
        while True:
            try:
                all_data = client.getData()
                time.sleep(0.5)
            except TimeoutError:
                print("Connection stopped")
        
    # client.writeData(all_data)


