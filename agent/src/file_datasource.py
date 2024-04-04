import random
from csv import reader
from datetime import datetime

from domain.parking import Parking
from domain.gps import Gps
from domain.accelerometer import Accelerometer
from domain.aggregated_data import AggregatedData


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_data = []
        self.gps_data = []
        self.parking_data = []
        self.last_read_index = 0

    def read(self) -> AggregatedData:
        if not self.accelerometer_data or not self.gps_data or not self.parking_data:
            print("No data available to read.")
            return None

        batch_size = random.randint(5, 25)

        start_index = self.last_read_index
        end_index = min(start_index + batch_size, len(self.accelerometer_data))
        if end_index >= len(self.accelerometer_data):
            print("Reached end of data, resetting read index.")
            self.last_read_index = 0  # Reset to start over

        print(f"Reading data from index {start_index} to {end_index}...")

        aggregated_data = []
        while start_index < len(self.accelerometer_data):
            accelerometer_rows = self.accelerometer_data[start_index:end_index]
            gps_rows = self.gps_data[start_index:end_index]
            parking_rows = self.parking_data[start_index:end_index]

            for accel_row, gps_row, parking_row in zip(accelerometer_rows, gps_rows, parking_rows):
                accelerometer = Accelerometer(*accel_row)
                gps = Gps(*gps_row)
                parking = Parking(parking_row[0], Gps(parking_row[1], parking_row[2]))
                aggregated_data.append(AggregatedData(accelerometer, gps, parking, datetime.now()))

            start_index = end_index
            end_index = min(start_index + batch_size, len(self.accelerometer_data))

            if end_index >= len(self.accelerometer_data):
                print("Reached end of data, resetting read index.")
                self.last_read_index = 0  # Reset to start over
            else:
                self.last_read_index = end_index

        print()
        print("Data reading completed.")
        return aggregated_data

    def start_reading(self):
        print("Starting to read files...")
        self.accelerometer_data = self.read_csv(self.accelerometer_filename)
        self.gps_data = self.read_csv(self.gps_filename)
        self.parking_data = self.read_csv(self.parking_filename)
        print("Reading started")

    def stop_reading(self):
        print("Stopping reading...")
        print("Reading stopped")
        self.accelerometer_data = []
        self.gps_data = []
        self.parking_data = []
        self.last_read_index = 0

    def read_csv(self, filename: str):
        print(f"Reading CSV file: {filename}")
        data = []
        with open(filename, 'r') as file:
            csv_reader = reader(file)
            next(csv_reader)
            for row in csv_reader:
                data.append([float(cell) for cell in row])
        print(data)
        print(f"Finished reading CSV file: {filename}")
        return data
