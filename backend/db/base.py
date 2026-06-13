# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base
from models.user import User, UserProfile, UserSkill
from models.career import CareerCategory, Career, Skill, CareerSkill
from models.assessment import AssessmentQuestion, AssessmentOption, Assessment, AssessmentResponse
from models.recommendation import CareerRecommendation
