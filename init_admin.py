import logging
import os
import sys
from sqlalchemy.orm import Session

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db.session import SessionLocal
from app.models.user import RoleEnum
from app.services.user_service import UserService
from app.schemas.user import UserCreate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_admin() -> None:
    db = SessionLocal()
    try:
        # Get admin credentials from environment variables or use defaults
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin")
        
        # Check if admin user already exists
        admin = UserService.get_by_email(db, email=admin_email)
        if admin:
            logger.info(f"Admin user {admin_email} already exists")
            return
        
        # Create admin user
        user_in = UserCreate(
            email=admin_email,
            password=admin_password,
            full_name="Admin",
            role=RoleEnum.ADMIN
        )
        
        UserService.create(db, user_in=user_in)
        logger.info(f"Admin user {admin_email} created with password: {admin_password}")
        logger.info("Please change the admin password after first login!")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Creating initial admin user")
    init_admin()
    logger.info("Initial admin user created") 