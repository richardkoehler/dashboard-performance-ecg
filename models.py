from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelPerformance(Base):
    __tablename__ = "model_performances"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    upload_time = Column(DateTime)
    performance_score = Column(Float)
    model_metadata = Column(JSON)  # Changed from metadata to model_metadata
    file_path = Column(String)
    
    def to_dict(self):
        return {
            "id": self.id,
            "model_name": self.model_name,
            "upload_time": self.upload_time.isoformat(),
            "performance_score": self.performance_score,
            "metadata": self.model_metadata,  # Keep the dict key as metadata for API consistency
            "file_path": self.file_path
        }
