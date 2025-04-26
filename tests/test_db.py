import pytest
from datetime import datetime
from app.db.models import Station, Temperature
from app.db.init_db import init_db

@pytest.fixture
def db_session():
    """Create a test database session."""
    session = init_db('sqlite:///:memory:')
    yield session
    session.close()

def test_create_station(db_session):
    """Test creating a station."""
    station = Station(
        name="Test Station",
        code="TEST001",
        latitude=40.7128,
        longitude=-74.0060,
        elevation=10.0
    )
    db_session.add(station)
    db_session.commit()
    
    # Verify station was created
    result = db_session.query(Station).first()
    assert result.name == "Test Station"
    assert result.code == "TEST001"
    assert result.latitude == 40.7128
    assert result.longitude == -74.0060
    assert result.elevation == 10.0

def test_create_temperature(db_session):
    """Test creating a temperature reading."""
    # First create a station
    station = Station(
        name="Test Station",
        code="TEST001",
        latitude=40.7128,
        longitude=-74.0060
    )
    db_session.add(station)
    db_session.commit()
    
    # Create temperature reading
    temp = Temperature(
        station_id=station.id,
        temperature=25.5,
        timestamp=datetime.utcnow()
    )
    db_session.add(temp)
    db_session.commit()
    
    # Verify temperature was created
    result = db_session.query(Temperature).first()
    assert result.station_id == station.id
    assert result.temperature == 25.5
    assert result.station.name == "Test Station"

def test_station_temperature_relationship(db_session):
    """Test the relationship between stations and temperatures."""
    # Create station
    station = Station(
        name="Test Station",
        code="TEST001",
        latitude=40.7128,
        longitude=-74.0060
    )
    db_session.add(station)
    db_session.commit()
    
    # Create multiple temperature readings
    temps = [
        Temperature(station_id=station.id, temperature=25.5, timestamp=datetime.utcnow()),
        Temperature(station_id=station.id, temperature=26.0, timestamp=datetime.utcnow()),
        Temperature(station_id=station.id, temperature=24.5, timestamp=datetime.utcnow())
    ]
    db_session.add_all(temps)
    db_session.commit()
    
    # Verify relationship
    station = db_session.query(Station).first()
    assert len(station.temperatures) == 3
    assert all(temp.station_id == station.id for temp in station.temperatures) 