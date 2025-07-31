from sqlalchemy import Column, Integer, String, Boolean, Date
from app.db.database import Base

class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String, nullable=False)
    date_of_interaction = Column(Date, nullable=False)  # ✅ FIXED: use correct field name
    key_discussion_points = Column(String, nullable=False)
    products_discussed = Column(String, nullable=True)
    follow_up_needed = Column(Boolean, default=False)
    original_message = Column(String, nullable=False)

__all__ = ["InteractionLog"]
