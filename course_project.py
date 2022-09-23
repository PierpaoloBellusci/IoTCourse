from lzma import is_check_supported
import sys
import hat
import mqtt_handler
from graceful_killer import GracefulKiller
from utils import getserial
import json
import time


def main():
    sense_hat = hat.hat()
    timestamp = int(time.time())

    
    cpu_serial_id = getserial()
    
    BROKER_url = "broker.hivemq.com"
    BROKER_PORT = 1883
    CLIEND_ID = cpu_serial_id

    mqtt_client = mqtt_handler.mqtt_handler(
        BROKER_url,
        BROKER_PORT,
        CLIEND_ID
    )
    
    mqtt_client.connect()
    time.sleep(1)
    is_connected = mqtt_client.check_connection()

    topic_env = f"IoTCourseData/{cpu_serial_id}/Environment"
    topic_motion = f"IoTCourseData/{cpu_serial_id}/Motion"

    grace_killer = GracefulKiller()

    if is_connected:
        print("client Connected to Broker !!")
        while not grace_killer.is_killed():
            env_data = sense_hat.get_env()
            env_data["timestamp"] = timestamp

            motion_data = sense_hat.get_movement()
            motion_data["timestamp"] = timestamp
            
            print(f"ENV_DATA: {env_data}")
            print(f"MOTION_DATA: {motion_data}")

            mqtt_client.publish(topic_env,json.dumps(env_data))
            mqtt_client.publish(topic_motion,json.dumps(motion_data))
            
            time.sleep(1)

        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
