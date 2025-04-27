from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from app.db.models import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Base repository class with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session

    def get(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return self.db_session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[ModelType]:
        """Get all records."""
        return self.db_session.query(self.model).all()

    def create(self, obj_in: dict) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj

    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        """Update a record."""
        db_obj = self.get(id)
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.db_session.commit()
            self.db_session.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Delete a record."""
        db_obj = self.get(id)
        if db_obj:
            self.db_session.delete(db_obj)
            self.db_session.commit()
            return True
        return False

    def bulk_create(self, objs_in: List[dict]) -> List[ModelType]:
        """Create multiple records in bulk."""
        db_objs = [self.model(**obj_in) for obj_in in objs_in]
        self.db_session.bulk_save_objects(db_objs)
        self.db_session.commit()
        return db_objs 