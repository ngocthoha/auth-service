from sqlalchemy import Boolean, Column, String, DateTime, Enum, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base_class import Base


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    SERVICE = "service"


class User(Base):
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    id = Column(String, primary_key=True, index=True)
    token = Column(String, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    
    user = relationship("User", back_populates="refresh_tokens") 