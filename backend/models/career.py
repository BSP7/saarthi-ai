from sqlalchemy import Column, String, Text, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db.base_class import Base

class CareerCategory(Base):
    __tablename__ = "career_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    careers = relationship("Career", back_populates="category")

class Career(Base):
    __tablename__ = "careers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("career_categories.id"), nullable=False)
    career_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    salary_range = Column(String(100), nullable=True)
    growth_outlook = Column(Text, nullable=True)
    required_skills = Column(JSON, nullable=True)

    category = relationship("CareerCategory", back_populates="careers")
    skills = relationship("CareerSkill", back_populates="career")
    recommendations = relationship("CareerRecommendation", back_populates="career")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    career_skills = relationship("CareerSkill", back_populates="skill")
    user_skills = relationship("UserSkill", back_populates="skill")

class CareerSkill(Base):
    __tablename__ = "career_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_id = Column(UUID(as_uuid=True), ForeignKey("careers.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    importance_level = Column(Integer, nullable=False)

    career = relationship("Career", back_populates="skills")
    skill = relationship("Skill", back_populates="career_skills")
