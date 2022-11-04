#!/usr/bin/env python3

import subprocess
import time
import json
from gpiozero import OutputDevice


ON_THRESHOLD = 60   # (degrees Celsius) Fan running at high speed at this temperature.
OFF_THRESHOLD = 50  # (degress Celsius) Fan running at low speed  at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 16       # Which GPIO pin you're using to control the fan.


def get_temp():
    """Get the core temperature.
    Run a shell script to get the core temp and parse the output.
    Raises:
        RuntimeError: if response cannot be parsed.
    Returns:
        float: The core temperature in degrees Celsius.
    """
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not parse temperature output.')

if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan = OutputDevice(GPIO_PIN)
    temp = get_temp()

    dFan = {
       'fan_speed': fan.value,
       'cpu_temp': temp,
       'on_threshold': ON_THRESHOLD,
       'off_threshold': OFF_THRESHOLD,
       'sleep_interval': SLEEP_INTERVAL
    }

    while True:
        temp = get_temp()

        # Fan running at high speed fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > ON_THRESHOLD and not fan.value:
            fan.on()

        # Run running at low speed if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif fan.value and temp < OFF_THRESHOLD:
            fan.off()

        # Save changed values into json file
        if (dFan['fan_speed'] != fan.value or dFan['cpu_temp'] != temp):
            dFan['fan_speed']  = fan.value
            dFan['cpu_temp']   = temp

            jsonString = json.dumps(dFan)
            jsonFile = open('/usr/share/hassio/homeassistant/files/ups_fan.json','w')
            jsonFile.write(jsonString)
            jsonFile.close()

        time.sleep(SLEEP_INTERVAL)
