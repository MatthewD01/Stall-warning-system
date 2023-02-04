import xpc 
from time import sleep
from time import monotonic

class XPlane:
    def __init__(self):
        self.client = xpc.XPlaneConnect()

    def connect(self):
        print("Estabilishing connection with XPlane")
        print("Setting up connection")

        try:
            self.client.getDREF("sim/test/float")
        except:
            print("There was a problem establishing a connection with client")
            print("Exiting")
            return

    # Function for Getting angle of attack and processing 
    def process_attack_angle(AoA : float):
        AoA_slope = AoA(-1) - AoA(-2) 
        
    # Function for stick shaker
    
    # Function for audio warning

    # Function for 




if __name__ == "__main__":
    client = XPlane()
    client.connect()
    state = True 
    AoA = []
    while state == True:
        AoA.append(client.client.getDREF("alpha")) # make as an array so I can get the previous value -> create a slope value 
        client.process_attack_angle(AoA)


