import time
from space_network_lib import SpaceEntity, SpaceNetwork,Packet,CommsError,TemporalInterferenceError,LinkTerminatedError,DataCorruptedError,OutOfRangeError

class Satellite(SpaceEntity):
    def __init__(self,name, distance_from_earth):
        super().__init__(name,distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"{self.name} received: {packet}")

class BrokenConnectionError(Exception):
    pass

class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxi):
        super().__init__(packet_to_relay,sender,proxi)

    def __repr__(self):
        return RelayPacket(f"railing[{self.data}] to {self.receiver} from {self.sender}")


# פונקציה המוודאת שליחת הודעה תוך כדי טיפול בשגיאות
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

        except LinkTerminatedError:
            print("link lost.")
            raise BrokenConnectionError

        except OutOfRangeError:
            print("Target out of range.")
            raise BrokenConnectionError


