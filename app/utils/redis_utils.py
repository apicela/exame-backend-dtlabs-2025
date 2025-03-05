# app/utils/redis_utils.py
from datetime import datetime
import json
from app.extensions import db, redis_client
from app.models.server import Server
from app.models.data import Data
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)
class RedisUtils:
    def __init__(self, app):
        self.app = app

    def process_data(self):
        while True:
            if redis_client.llen('data_queue') > 0:
                data = redis_client.lpop('data_queue')
                logging.debug(f"Data: {data}")
                if data:
                    server_data_str, new_data_str = data.decode('utf-8').split('|')

                    try:
                        server_data = json.loads(server_data_str)
                        new_data_dict = json.loads(new_data_str)
                        new_data = Data(
                            server_ulid=new_data_dict['server_ulid'],
                            timestamp=datetime.fromisoformat(new_data_dict['timestamp']),
                            temperature=new_data_dict['temperature'],
                            humidity=new_data_dict['humidity'],
                            voltage=new_data_dict['voltage'],
                            current=new_data_dict['current']
                        )


                        with self.app.app_context():
                            server = Server.query.filter_by(server_ulid=server_data['server_ulid']).first()
                            server.last_ping = datetime.fromisoformat(server_data['last_ping']) if server_data['last_ping'] else None
                            server.last_data_timestamp = datetime.fromisoformat(server_data['last_data_timestamp']) if server_data['last_data_timestamp'] else None
                            db.session.add(new_data)
                            db.session.commit()

                    except json.JSONDecodeError as e:
                        logging.debug(f"Error decoding JSON: {e}")
                        continue

            sleep(2)