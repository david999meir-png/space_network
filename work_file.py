import time

from space_network_lib import SpaceEntity, SpaceNetwork,Packet,CommsError,TemporalInterferenceError,LinkTerminatedError,DataCorruptedError,OutOfRangeError
from time import sleep

class Satellite(SpaceEntity):
    def __init__(self,name, distance_from_earth):
        super().__init__(name,distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"{self.name} received: {packet}")


my_network = SpaceNetwork(level=2)

sat1 = Satellite("sat1",100)
sat2 =Satellite("sat2",200)

my_massage = Packet("how are you?",sat1,sat2)



def attempt_transmission(packet):
    while True:
        try:
            my_network.send(my_massage)
            break
        except TemporalInterferenceError:
            print("interference, waiting...")
            time.sleep(2)
            continue
        except DataCorruptedError:
            print("data corrupted, retrying...")
            continue

attempt_transmission(my_massage)