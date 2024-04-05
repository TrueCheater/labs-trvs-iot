from paho.mqtt import client as mqtt_client
import time

from schema.parking_schema import ParkingSchema
from schema.gps_schema import GpsSchema
from schema.accelerometer_schema import AccelerometerSchema
from file_datasource import FileDatasource
import config


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client, accel_topic, gps_topic, parking_topic, datasource, delay):
    datasource.start_reading()
    while True:
        time.sleep(delay)
        data = datasource.read()
        for datum in data:
            accel_msg = AccelerometerSchema().dumps(datum.accelerometer)
            mqtt_publish(client, accel_topic, accel_msg)

            gps_msg = GpsSchema().dumps(datum.gps)
            mqtt_publish(client, gps_topic, gps_msg)

            parking_msg = ParkingSchema().dumps(datum.parking)
            mqtt_publish(client, parking_topic, parking_msg)


def mqtt_publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource(
        "data/accelerometer.csv",
        "data/gps.csv",
        "data/parking.csv"
    )
    # Infinity publish data
    publish(
        client,
        config.MQTT_ACCELEROMETER_TOPIC,
        config.MQTT_GPS_TOPIC,
        config.MQTT_PARKING_TOPIC,
        datasource,
        config.DELAY
    )


if __name__ == '__main__':
    run()
