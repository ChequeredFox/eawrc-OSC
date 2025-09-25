import eawrcsdk
import time
import yaml
import argparse

from pythonosc import udp_client


class Config:

    def __init__(self, target_file):
        self.file = target_file
        self.config = []
        self.loadYamlConfig()

    def loadYamlConfig(self):
        with open(self.file, 'r') as file:
            self._config = yaml.safe_load(file)
            self.settings = self._config["config"]

class State:
    def __init__(self):
        self.last_gear_tick = -1

def loop(wrc, client, state):
    gear = wrc['vehicle_gear_index']
    if gear != state.last_gear_tick: #only send gear change if gear has changed
        state.last_gear_tick = gear
        client.send_message("/car/gear", gear)

    wheelAngle = wrc['vehicle_steering']
    vert = wrc['vehicle_acceleration_y']
    speed = wrc['vehicle_speed']

    client.send_message("/car/steering", wheelAngle)
    client.send_message("/car/speed", speed)
    client.send_message("/motion/vertical_accel", vert)



    w, x, y, z = wrc.get_vehicle_quaternion()

    client.send_message("/motion/w", w)
    client.send_message("/motion/x", x)
    client.send_message("/motion/y", y)
    client.send_message("/motion/z", z)   

if __name__ == "__main__":
    config = Config("config.yaml")

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=config.settings['destination_ip'],
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=config.settings['port'],
        help="The port of the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    state = State()
    wrc = eawrcsdk.EAWRCSDK()
    wrc.connect()
    print("client connected")
    while True:
        try:
            wrc.freeze_buffer_latest() #Freeze telemmetry data so all data retrieved is from the same telemmetry packet
            if wrc['game_total_time']: #check if data exists first
                loop(wrc, client, state)
            time.sleep(1/30)
        except KeyboardInterrupt:
            break
    wrc.close()
    print("client closed")