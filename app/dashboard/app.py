from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.db.init_db import init_db
from app.db.repositories import StationRepository, TemperatureRepository

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Initialize database
    db_session = init_db('sqlite:///../db/weather.db')
    
    @app.route('/api/cities', methods=['GET'])
    def get_cities():
        """Get list of all available cities."""
        try:
            station_repo = StationRepository(db_session)
            stations = station_repo.get_all()
            
            cities = [
                {
                    'id': station.id,
                    'name': station.name,
                    'code': station.code,
                    'latitude': station.latitude,
                    'longitude': station.longitude
                }
                for station in stations
            ]
            
            return jsonify(cities)
        except SQLAlchemyError as e:
            return jsonify({'error': 'Database error occurred'}), 500
        except Exception as e:
            return jsonify({'error': 'An unexpected error occurred'}), 500

    @app.route('/api/temperature-comparison', methods=['GET'])
    def get_temperature_comparison():
        """Get temperature comparison data for two cities over a date range."""
        try:
            # Get query parameters
            city1_id = request.args.get('city1_id', type=int)
            city2_id = request.args.get('city2_id', type=int)
            start_date = request.args.get('start_date', type=str)
            end_date = request.args.get('end_date', type=str)

            # Validate parameters
            if not all([city1_id, city2_id, start_date, end_date]):
                return jsonify({'error': 'Missing required parameters'}), 400

            # Convert dates
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Get temperature data
            temp_repo = TemperatureRepository(db_session)
            city1_temps = temp_repo.get_by_station_and_date_range(city1_id, start_date, end_date)
            city2_temps = temp_repo.get_by_station_and_date_range(city2_id, start_date, end_date)

            # Process data
            hourly_data = {}
            for temp in city1_temps + city2_temps:
                hour = temp.timestamp.hour
                if hour not in hourly_data:
                    hourly_data[hour] = {'city1': [], 'city2': []}
                
                if temp.station_id == city1_id:
                    hourly_data[hour]['city1'].append(temp.temperature)
                else:
                    hourly_data[hour]['city2'].append(temp.temperature)

            # Calculate averages and differences
            result = []
            for hour in range(24):
                city1_avg = sum(hourly_data[hour]['city1']) / len(hourly_data[hour]['city1']) if hourly_data[hour]['city1'] else None
                city2_avg = sum(hourly_data[hour]['city2']) / len(hourly_data[hour]['city2']) if hourly_data[hour]['city2'] else None
                
                if city1_avg is not None and city2_avg is not None:
                    difference = city1_avg - city2_avg
                else:
                    difference = None

                result.append({
                    'hour': hour,
                    'city1_temperature': city1_avg,
                    'city2_temperature': city2_avg,
                    'difference': difference
                })

            # Find min/max differences
            valid_differences = [r['difference'] for r in result if r['difference'] is not None]
            if valid_differences:
                min_diff = min(valid_differences)
                max_diff = max(valid_differences)
                min_hour = next(r['hour'] for r in result if r['difference'] == min_diff)
                max_hour = next(r['hour'] for r in result if r['difference'] == max_diff)
            else:
                min_diff = max_diff = min_hour = max_hour = None

            return jsonify({
                'hourly_data': result,
                'min_difference': {
                    'hour': min_hour,
                    'difference': min_diff
                },
                'max_difference': {
                    'hour': max_hour,
                    'difference': max_diff
                }
            })

        except SQLAlchemyError as e:
            return jsonify({'error': 'Database error occurred'}), 500
        except Exception as e:
            return jsonify({'error': 'An unexpected error occurred'}), 500
    
    return app 