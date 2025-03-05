from ..models import Data
from ..utils import ErrorResponse
from .server_service import ServerService
from app.extensions import db, redis_client
from sqlalchemy import func
from datetime import datetime, timedelta
import json
import logging

logging.basicConfig(level=logging.DEBUG)

class DataService:
    def insert_data(server_ulid, timestamp, temperature, humidity, voltage, current):
        server = ServerService.get_server(server_ulid)
        if not timestamp:
            raise ErrorResponse("Timestamp is required", 400)
        try:
            datetime.fromisoformat(timestamp)
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        except:
            raise ErrorResponse("Invalid timestamp", 400)
        
        if not temperature and not humidity:
            raise ErrorResponse("Temperature or humidity data is required", 400)

        
        if humidity:
            humidity = float(humidity)  # Convert humidity to a float if it's a string
            if humidity < 0 or humidity > 100:
                raise ErrorResponse("Invalid humidity value", 400)


    # Frequency check
        if server.last_data_timestamp:
            time_diff = timestamp - server.last_data_timestamp
            if time_diff < timedelta(seconds=0.1) or time_diff > timedelta(seconds=1):
                raise ErrorResponse("Data frequency out of range (1 Hz to 10 Hz)", 400)

        server.last_ping = datetime.now()
        server.last_data_timestamp = timestamp

        new_data = Data(
            server_ulid=server_ulid,
            timestamp=timestamp,
            temperature=temperature,
            humidity=humidity,
            voltage=voltage,
            current=current
        )

        data_dict = {
            'server_ulid': new_data.server_ulid,
            'timestamp': new_data.timestamp.isoformat(),
            'temperature': new_data.temperature,
            'humidity': new_data.humidity,
            'voltage': new_data.voltage,
            'current': new_data.current
        }


        serialized_data = json.dumps(data_dict)
        serialized_server = json.dumps({
            'last_ping': server.last_ping.isoformat(),
            'last_data_timestamp': server.last_data_timestamp.isoformat(),
            'server_ulid': server.server_ulid
        })
        redis_client.rpush('data_queue', f"{serialized_server}|{serialized_data}")

        return {'message': 'Data inserted successfully'}
    
    @staticmethod
    def get_data(current_user, server_ulid=None, start_time=None, end_time=None, sensor_type=None, aggregation=None):
        logging.debug(f"get_data: {current_user}, {server_ulid}, {start_time}, {end_time}, {sensor_type}, {aggregation}")   
        query = db.session.query(Data.timestamp)

        valid_sensors = ['temperature', 'humidity', 'voltage', 'current']

        if sensor_type:
            if sensor_type not in valid_sensors:
                return {"error": f"Sensor inválido: {sensor_type}"}, 400
            query = query.add_columns(getattr(Data, sensor_type))
        else:
            for sensor in valid_sensors:
                query = query.add_columns(getattr(Data, sensor))

        filters = []
        if server_ulid:
            filters.append(Data.server_ulid == server_ulid)

        from datetime import datetime
        def parse_time(value):
            if isinstance(value, str):
                try:
                    return datetime.fromisoformat(value)
                except ValueError:
                    return None
            return value  

        start_time = parse_time(start_time)
        end_time = parse_time(end_time)

        if start_time and end_time:
            filters.append(and_(Data.timestamp >= start_time, Data.timestamp <= end_time))

        if filters:
            query = query.filter(*filters)

        logging.debug(f"SQL Query: {query}")

        results = query.all()

        # Construindo a resposta removendo valores None
        response = [
            {key: value for key, value in {
                'timestamp': result[0], 
                **({sensor: result[idx + 1] for idx, sensor in enumerate(valid_sensors) if result[idx + 1] is not None} if not sensor_type else {sensor_type: result[1] if result[1] is not None else None})
            }.items() if value is not None}
            for result in results
        ]
        
        return response

