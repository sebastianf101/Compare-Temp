from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models import Station
from .base import BaseRepository

class StationRepository(BaseRepository[Station]):
    """Repository for station operations."""
    
    def __init__(self, db_session: Session):
        super().__init__(Station, db_session)

    def get_by_code(self, code: str) -> Optional[Station]:
        """Get a station by its code."""
        return self.db_session.query(Station).filter(Station.code == code).first()

    def get_by_name(self, name: str) -> Optional[Station]:
        """Get a station by its name."""
        return self.db_session.query(Station).filter(Station.name == name).first()

    def get_by_location(self, latitude: float, longitude: float) -> List[Station]:
        """Get stations near a specific location."""
        # Using a simple distance calculation (can be improved with PostGIS for PostgreSQL)
        return self.db_session.query(Station).filter(
            Station.latitude.between(latitude - 0.1, latitude + 0.1),
            Station.longitude.between(longitude - 0.1, longitude + 0.1)
        ).all()

    def upsert_by_code(self, station_data: dict) -> Station:
        """Update or insert a station by its code."""
        station = self.get_by_code(station_data['code'])
        if station:
            return self.update(station.id, station_data)
        return self.create(station_data) 