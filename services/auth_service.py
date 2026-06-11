import bcrypt
from database.db import get_db_session
from database.models import User
from utils.helpers import is_valid_email, is_strong_password

class AuthService:
    """Handles user authentication, signup, and login."""

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def signup(full_name: str, email: str, password: str, **kwargs) -> dict:
        """Registers a new user in the database."""
        if not is_valid_email(email):
            return {"success": False, "message": "Invalid email format."}
        
        if not is_strong_password(password):
            return {"success": False, "message": "Password must be at least 8 characters long."}

        db = get_db_session()
        try:
            # Check if user exists
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                return {"success": False, "message": "Email already registered."}

            # Create new user
            new_user = User(
                full_name=full_name,
                email=email,
                password_hash=AuthService.hash_password(password),
                **kwargs
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Prepare session data
            user_data = {
                "id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email
            }
            return {"success": True, "message": "Signup successful.", "user": user_data}
            
        except Exception as e:
            db.rollback()
            return {"success": False, "message": f"An error occurred: {str(e)}"}
        finally:
            db.close()

    @staticmethod
    def login(email: str, password: str) -> dict:
        """Authenticates a user and returns their info."""
        db = get_db_session()
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user or not AuthService.verify_password(password, user.password_hash):
                return {"success": False, "message": "Invalid email or password."}
            
            user_data = {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "currency": user.preferred_currency
            }
            return {"success": True, "message": "Login successful.", "user": user_data}
        except Exception as e:
            return {"success": False, "message": f"An error occurred: {str(e)}"}
        finally:
            db.close()

    @staticmethod
    def update_profile(user_id: int, updates: dict) -> dict:
        """Updates user profile information."""
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"success": False, "message": "User not found."}
                
            for key, value in updates.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                    
            db.commit()
            return {"success": True, "message": "Profile updated successfully."}
        except Exception as e:
            db.rollback()
            return {"success": False, "message": f"An error occurred: {str(e)}"}
        finally:
            db.close()
