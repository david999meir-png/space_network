import time
from space_network_lib import SpaceEntity, SpaceNetwork,Packet,CommsError,TemporalInterferenceError,LinkTerminatedError,DataCorruptedError,OutOfRangeError

class Satellite(SpaceEntity):
    def __init__(self,name, distance_from_earth):
        super().__init__(name,distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"{self.name} received: {packet}")






def attempt_transmission(packet,network):
    while True:
        try:
            network.send(packet)
            break
        except TemporalInterferenceError:
            print("interference, waiting...")
            time.sleep(2)
            continue
        except DataCorruptedError:
            print("data corrupted, retrying...")
            continue

