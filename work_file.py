import time
from space_network_lib import SpaceEntity, SpaceNetwork,Packet,CommsError,TemporalInterferenceError,LinkTerminatedError,DataCorruptedError,OutOfRangeError

class Satellite(SpaceEntity):
    def __init__(self,name, distance_from_earth):
        super().__init__(name,distance_from_earth)


    def receive_signal(self, packet: Packet):
        if isinstance(packet,RelayPacket):
            print(f"Unwrapping and forwarding to {packet.receiver}")
            packet = packet.data
            attempt_transmission(packet)
        else:
            print(f"Final destination reached: {packet.data}")

class BrokenConnectionError(Exception):
    pass

my_network = SpaceNetwork(level=3)


class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxi):
        super().__init__(packet_to_relay,sender,proxi)

    def __repr__(self):
        return RelayPacket(f"railing[{self.data}] to {self.receiver} from {self.sender}")


# פונקציה המוודאת שליחת הודעה תוך כדי טיפול בשגיאות
def attempt_transmission(packet):
    while True:
        try:
            my_network.send(packet)
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


def smart_send_packet(spaces:list, massage:Packet):
    sender = massage.sender
    receiver = massage.receiver
    for space in spaces:
        if receiver.distance_from_earth - sender.distance_from_earth >= 150:
            if abs(space.distance_from_earth - receiver.distance_from_earth) >= 150:
                continue
            else:
                massage = RelayPacket(massage,space,receiver)
                receiver = space
        else:
            break
    RelayPacket(massage,sender,receiver)
