# backend/app/scansione_documenti/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import Base

# class Scansione(Base):
#     __tablename__ = "scans"
#     __table_args__ = {"schema": "scansione_documenti"}  # 🔥 Qui specifichiamo lo schema
#
#     id = Column(Integer, primary_key=True)
#     filename = Column(String, nullable=False)
#     file_path = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP, nullable=False)
