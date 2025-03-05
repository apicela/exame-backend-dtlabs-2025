from ..models import Data
from ..utils import ErrorResponse
from .server_service import ServerService
from app.extensions import db, redis_client
from sqlalchemy import func
from datetime import datetime, timedelta
import json

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
        serialized_server = json.dumps(server.to_dict())
        redis_client.rpush('data_queue', f"{serialized_server}|{serialized_data}")
        db.session.add(server)
        db.session.add(new_data)
        db.commit()
        return {'message': 'Data inserted successfully'}
    
    def get_data(current_user, server_ulid, start_time, end_time, sensor_type, aggregation):
        query = db.session.query(Data.timestamp, getattr(Data, sensor_type)).filter(getattr(Data, sensor_type).isnot(None))

        if server_ulid:
            query = query.filter(Data.server_ulid == server_ulid)
        if start_time and end_time:
            query = query.filter(Data.timestamp.between(start_time, end_time))
        
        if aggregation:
            if aggregation == 'minute':
                time_trunc = func.date_trunc('minute', Data.timestamp)
            elif aggregation == 'hour':
                time_trunc = func.date_trunc('hour', Data.timestamp)
            elif aggregation == 'day':
                time_trunc = func.date_trunc('day', Data.timestamp)
            else:
                raise ErrorResponse("Invalid aggregation", 400)

            query = db.session.query(
                time_trunc.label("timestamp"),
                func.avg(getattr(Data, sensor_type)).label(sensor_type)
            ).group_by(time_trunc)
        
        results = query.all()

        return [{'timestamp': result[0], sensor_type: result[1]} for result in results]