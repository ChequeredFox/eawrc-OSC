
# EAWRC-OSC

An application utilizing [py-eawrc-sdk](https://github.com/ChequeredFox/py-eawrc-sdk) to capture telemetry output by EA WRC and forward it via OSC.

Intended to be used as middleware between EA WRC and Warudo



## Installation
- [Python 3.9+](https://www.python.org/downloads/)
- cd to downloaded repository `pip install -r requirements.txt`
- Run main.py

NOTE - EA WRC must be launched at least once to generate telemmetry configuration files found in `%UserProfile%/Documents/My Games/WRC/telemetry/`


## Usage

Outputs 8 OSC messages to 127.0.0.1:19190 (configurable in config.yaml)

- "/car/gear" NOTE: only outputs if gear has changed
- "/car/steering"
- "/car/speed"
- "/motion/vertical_accel"
- "/motion/w"
- "/motion/x"
- "/motion/y"
- "/motion/z"