from sqlalchemy import Column, ForeignKey, Integer, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db.base_class import Base

class CareerRecommendation(Base):
    __tablename__ = "career_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False)
    career_id = Column(UUID(as_uuid=True), ForeignKey("careers.id"), nullable=False)
    match_score = Column(DECIMAL(5, 2), nullable=False)
    rank_position = Column(Integer, nullable=False)

    assessment = relationship("Assessment", back_populates="recommendations")
    career = relationship("Career", back_populates="recommendations")
