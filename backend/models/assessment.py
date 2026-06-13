from sqlalchemy import Column, String, Text, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from db.base_class import Base

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_text = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    difficulty = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    options = relationship("AssessmentOption", back_populates="question")
    responses = relationship("AssessmentResponse", back_populates="question")

class AssessmentOption(Base):
    __tablename__ = "assessment_options"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("assessment_questions.id"), nullable=False)
    option_text = Column(Text, nullable=False)
    score_weight = Column(Integer, nullable=False)

    question = relationship("AssessmentQuestion", back_populates="options")
    responses = relationship("AssessmentResponse", back_populates="selected_option")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    total_score = Column(Integer, nullable=True)

    user = relationship("User", back_populates="assessments")
    responses = relationship("AssessmentResponse", back_populates="assessment")
    recommendations = relationship("CareerRecommendation", back_populates="assessment")

class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("assessment_questions.id"), nullable=False)
    selected_option_id = Column(UUID(as_uuid=True), ForeignKey("assessment_options.id"), nullable=False)

    assessment = relationship("Assessment", back_populates="responses")
    question = relationship("AssessmentQuestion", back_populates="responses")
    selected_option = relationship("AssessmentOption", back_populates="responses")
