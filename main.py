from space_network_lib import SpaceEntity, SpaceNetwork,Packet,CommsError,TemporalInterferenceError,LinkTerminatedError,DataCorruptedError,OutOfRangeError
from work_file import Satellite,attempt_transmission,BrokenConnectionError,RelayPacket



sat1 = Satellite("sat1",100)
sat2 =Satellite("sat2",200)

my_massage = Packet("how are you?",sat1,sat2)

earth = Satellite("Earth", 0)




try:
    attempt_transmission(my_massage)

except BrokenConnectionError:
    print("Transmission failed.")