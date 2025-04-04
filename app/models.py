from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class ModelPerformance(Base):
    __tablename__ = "model_performances"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    upload_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    performance_score = Column(Float)
    model_info = Column(String)  # Changed from metadata to model_info
    file_path = Column(String)

    def to_dict(self) -> dict[str, str | float | int | datetime]:
        return {
            "id": self.id,
            "model_name": self.model_name,
            "upload_time": self.upload_time.isoformat(),
            "performance_score": self.performance_score,
            "metadata": self.model_info,
            "file_path": self.file_path,
        }
