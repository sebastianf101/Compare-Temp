from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.models import Temperature
from .base import BaseRepository

class TemperatureRepository(BaseRepository[Temperature]):
    """Repository for temperature operations."""
    
    def __init__(self, db_session: Session):
        super().__init__(Temperature, db_session)

    def get_by_station(self, station_id: int) -> List[Temperature]:
        """Get all temperature readings for a station."""
        return self.db_session.query(Temperature).filter(
            Temperature.station_id == station_id
        ).all()

    def get_by_station_and_date_range(
        self, 
        station_id: int, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Temperature]:
        """Get temperature readings for a station within a date range."""
        return self.db_session.query(Temperature).filter(
            and_(
                Temperature.station_id == station_id,
                Temperature.timestamp >= start_date,
                Temperature.timestamp <= end_date
            )
        ).all()

    def get_latest_by_station(self, station_id: int) -> Optional[Temperature]:
        """Get the latest temperature reading for a station."""
        return self.db_session.query(Temperature).filter(
            Temperature.station_id == station_id
        ).order_by(Temperature.timestamp.desc()).first()

    def bulk_create_temperatures(self, temperatures: List[dict]) -> List[Temperature]:
        """Create multiple temperature readings in bulk."""
        return self.bulk_create(temperatures) 