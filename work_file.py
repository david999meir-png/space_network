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

class SecurityBreachError(Exception):
    pass

my_network = SpaceNetwork(level=3)


class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxi):
        super().__init__(packet_to_relay,sender,proxi)

    def __repr__(self):
        return f"RelayPacket(Relaying[{self.data}] to {self.receiver.name} via {self.sender.name})"


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


def smart_send_packet(spaces: list, massage: Packet):
    sender = massage.sender
    receiver = massage.receiver
    def get_dist(s):
        return s.distance_from_earth
    spaces.sort(key=get_dist)

    path = []
    start_p = min(sender.distance_from_earth, receiver.distance_from_earth)
    end_p = max(sender.distance_from_earth, receiver.distance_from_earth)
    for s in spaces:
        if start_p < s.distance_from_earth < end_p:
            path.append(s)

    if sender.distance_from_earth > receiver.distance_from_earth:
        path.reverse()

    if len(path) > 0:
        massage.sender = path[-1]
    path.reverse()
    current_target = receiver

    for space in path:
        massage = RelayPacket(massage, space, current_target)
        current_target = space
    new_massage = RelayPacket(massage, sender, current_target)
    attempt_transmission(new_massage)



# הצפנת פקטות
class EncryptedPacket(Packet):
    def __init__(self,key,data,sender, receiver):
        super().__init__(data,sender,receiver)
        self.__key = key
        temp_massage =""
        for i, v in enumerate(self.data):
            temp_word = ord(v) ^ ord(self.__key[i % len(self.__key)])
            temp_massage += chr(temp_word)
        self.data = temp_massage


    def decrypt(self,key):
        if key == self.__key:
            real_massage = ""
            for i, v in enumerate(self.data):
                temp = ord(v) ^ ord(self.__key[i % len(self.__key)])
                real_massage += chr(temp)
            return real_massage
        else:
            raise SecurityBreachError("key value not good!")


