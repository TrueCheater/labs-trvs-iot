import json
import logging
from typing import List
import requests

from app.entities.processed_agent_data import ProcessedAgentData

from app.interfaces.store_api_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """

        # Make a POST request to the Store API endpoint with the processed data
        url = f"{self.api_base_url}/processed_agent_data"
        headers = {"Content-Type": "application/json"}
        # Convert datetime objects to strings
        processed_data_list = [{
            "road_state": data.road_state,
            "agent_data": {
                "accelerometer": data.agent_data.accelerometer.dict(),
                "gps": data.agent_data.gps.dict(),
                "timestamp": data.agent_data.timestamp.isoformat()
            }
        } for data in processed_agent_data_batch]
        data = json.dumps(processed_data_list)
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            logging.info("Data saved successfully")
            return True
        else:
            logging.error(f"Failed to save data: {response.text}")
            return False
