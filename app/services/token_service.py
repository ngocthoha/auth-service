from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from typing import Optional, Tuple

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.models.user import User, RefreshToken
from app.schemas.token import TokenPayload


class TokenService:
    @staticmethod
    def create_tokens(user: User, db: Session) -> Tuple[str, str]:
        """
        Create both access token and refresh token for a user
        """
        # Create access token
        access_token = create_access_token(
            subject=user.id,
            role=user.role
        )
        
        # Create refresh token
        refresh_token_str = create_refresh_token()
        refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Store refresh token in database
        db_refresh_token = RefreshToken(
            id=str(uuid.uuid4()),
            token=refresh_token_str,
            expires_at=refresh_token_expires,
            user_id=user.id
        )
        db.add(db_refresh_token)
        db.commit()
        
        return access_token, refresh_token_str
    
    @staticmethod
    def validate_access_token(token: str) -> Optional[TokenPayload]:
        """
        Decode and validate the JWT access token
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            
            if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
                return None
                
            return token_data
        except JWTError:
            return None
    
    @staticmethod
    def refresh_tokens(refresh_token: str, db: Session) -> Optional[Tuple[str, str]]:
        """
        Generate new access and refresh tokens using a valid refresh token
        """
        # Find the refresh token in the database
        db_refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token
        ).first()
        
        if not db_refresh_token:
            return None
        
        # Check if the refresh token has expired
        if db_refresh_token.expires_at < datetime.utcnow():
            db.delete(db_refresh_token)
            db.commit()
            return None
        
        # Get the user
        user = db_refresh_token.user
        
        # Delete the old refresh token
        db.delete(db_refresh_token)
        db.commit()
        
        # Create new tokens
        return TokenService.create_tokens(user, db)
    
    @staticmethod
    def revoke_refresh_token(refresh_token: str, db: Session) -> bool:
        """
        Revoke a refresh token (used for logout)
        """
        db_refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token
        ).first()
        
        if not db_refresh_token:
            return False
        
        db.delete(db_refresh_token)
        db.commit()
        return True
        
    @staticmethod
    def revoke_all_user_tokens(user_id: str, db: Session) -> bool:
        """
        Revoke all refresh tokens for a user (used for force logout)
        """
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id
        ).delete()
        db.commit()
        return True 