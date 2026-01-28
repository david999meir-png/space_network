from space_network_lib import SpaceEntity, SpaceNetwork,Packet,CommsError,TemporalInterferenceError,LinkTerminatedError,DataCorruptedError,OutOfRangeError
from work_file import Satellite,attempt_transmission,BrokenConnectionError,RelayPacket


earth = Satellite("Earth", 0)
sat1 = Satellite("sat1",100)
sat2 =Satellite("sat2",200)
sat3 =Satellite("sat3",300)
sat4 =Satellite("sat4",400)


my_massage = Packet("how are you?",sat1,sat2)


p_final = Packet("hello from earth!",sat1,sat2)

p_earth_to_sat1 = RelayPacket(p_final,earth,sat1)


try:
    attempt_transmission(my_massage)

except BrokenConnectionError:
    print("Transmission failed.")

print("*"*20)

try:
    attempt_transmission(p_earth_to_sat1)

except BrokenConnectionError:
    print("Transmission failed.")