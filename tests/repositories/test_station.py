import pytest
from datetime import datetime
from app.repositories.station import StationRepository

def test_get_by_code(db_session):
    """Test getting a station by code."""
    repo = StationRepository(db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    repo.create(station_data)
    station = repo.get_by_code('TEST001')
    assert station is not None
    assert station.name == 'Test Station'

def test_get_by_name(db_session):
    """Test getting a station by name."""
    repo = StationRepository(db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    repo.create(station_data)
    station = repo.get_by_name('Test Station')
    assert station is not None
    assert station.code == 'TEST001'

def test_get_by_location(db_session):
    """Test getting stations by location."""
    repo = StationRepository(db_session)
    stations_data = [
        {
            'name': 'Station 1',
            'code': 'ST001',
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        {
            'name': 'Station 2',
            'code': 'ST002',
            'latitude': 40.7129,
            'longitude': -74.0061
        },
        {
            'name': 'Station 3',
            'code': 'ST003',
            'latitude': 40.0,
            'longitude': -74.0
        }
    ]
    for data in stations_data:
        repo.create(data)
    
    stations = repo.get_by_location(40.7128, -74.0060)
    assert len(stations) == 2
    assert {s.code for s in stations} == {'ST001', 'ST002'}

def test_upsert_by_code(db_session):
    """Test upserting a station by code."""
    repo = StationRepository(db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    
    # First create
    station = repo.upsert_by_code(station_data)
    assert station.name == 'Test Station'
    
    # Then update
    updated_data = {
        'name': 'Updated Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    updated = repo.upsert_by_code(updated_data)
    assert updated.name == 'Updated Station'
    assert updated.id == station.id 