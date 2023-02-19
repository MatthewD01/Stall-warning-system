import xpc
import time
import csv
from itertools import zip_longest
import serial





class XPlane:

    def __init__(self):
        self.client = xpc.XPlaneConnect()
        self.ser = serial.Serial("COM3", 9600)
        self.data_refs = {
            "AoA" : [],
            "Pitch" : [],
            "Flight path" : [], 
            "Velocity" : [],
            "Time" : []
        }
    
            

    def getData(self):
                
        AoA = self.client.getDREF("sim/flightmodel2/misc/AoA_angle_degrees")
        pitch = self.client.getDREF("sim/flightmodel/position/theta")
        flight_path = self.client.getDREF("sim/flightmodel/position/hpath")
        velocity = self.client.getDREF("sim/flightmodel/forces/vz_air_on_acf")
            
        self.data_refs["AoA"].append(AoA)
        self.data_refs["Flight path"].append(pitch)
        self.data_refs["Pitch"].append(flight_path)
        self.data_refs["Velocity"].append(velocity)
        self.data_refs["Time"].append(time.monotonic)
        print(self.data_refs)
        
    
    def writeData(self):
        with open('datarefs.csv', 'w', newline='') as file:
        
          writer = csv.writer(file)
          writer.writerow(self.data_refs.keys())
          rows = list(zip_longest(*self.data_refs.values()))
          writer.writerows(rows)

    def warning_calculations(self):
        """""
        Uses the dictionary to calculate the current and previous slopes of the AoA
        Outputs a corresponding number to talk to the arduino
        """""
        
        attack_angle = self.data_refs["AoA"]
        current_time = self.data_refs["Time"]

        if len(attack_angle) > 1:
            warning_value = (attack_angle[-1]-attack_angle[-2])/(current_time[-1] - current_time[2])
            if warning_value >= 2 and 5 < attack_angle[-1] < 10:
                return 1
            elif warning_value >= 2 and attack_angle[-1] > 10:
                return 2
            else:
                return 0
        

        return warning_value
        
    
if __name__ == "__main__":
        refs = ["AoA", "Flight path", "Pitch", "Velocity"]
        client = XPlane()
        
        while True:
            try:
                all_data = client.getData()

                warning_value = client.warning_calculations()
                client.ser.write([warning_value])

                client.writeData(all_data)
                print(all_data)

            except TimeoutError:
                print("Connection stopped")
        
        
        
    


