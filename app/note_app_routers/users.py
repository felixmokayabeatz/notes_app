from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import schemas, crud, database
from app.auth import create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

# Register
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.create_user(db, user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user



from fastapi import BackgroundTasks, HTTPException, status, Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import secrets
import string
from app import models, database
from app.auth import get_password_hash  # Import from your auth file

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME="your_email@example.com",
    MAIL_PASSWORD="your_email_password",
    MAIL_FROM="noreply@noteflow.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

# Password reset token generation
def generate_reset_token():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

# Store reset tokens temporarily (in production, use Redis or database)
reset_tokens = {}

# Password reset request endpoint
@router.post("/forgot-password")
async def forgot_password(
    request: dict,  # Changed to accept JSON body
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    email = request.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        # Generate reset token
        reset_token = generate_reset_token()
        reset_tokens[reset_token] = {
            "user_id": user.id,
            "expires": datetime.now(timezone.utc) + timedelta(hours=1)  # Fixed UTC issue
        }
        
        # Send email with reset link
        reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
        
        message = MessageSchema(
            subject="Password Reset Request - NoteFlow",
            recipients=[email],
            body=f"""
            Hello {user.email},
            
            You requested a password reset for your NoteFlow account.
            
            Click the link below to reset your password:
            {reset_link}
            
            This link will expire in 1 hour.
            
            If you didn't request this, please ignore this email.
            
            Best regards,
            NoteFlow Team
            """,
            subtype="plain"
        )
        
        background_tasks.add_task(send_reset_email, message)
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent"}

async def send_reset_email(message: MessageSchema):
    fm = FastMail(conf)
    await fm.send_message(message)

# Password reset confirmation endpoint
@router.post("/reset-password")
async def reset_password(
    request: dict,  # Changed to accept JSON body
    db: Session = Depends(database.get_db)
):
    token = request.get("token")
    new_password = request.get("new_password")
    
    if not token or not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token and new password are required"
        )
    
    # Validate token
    if token not in reset_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    token_data = reset_tokens[token]
    
    # Check if token expired (using timezone-aware datetime)
    if datetime.now(timezone.utc) > token_data["expires"]:
        del reset_tokens[token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Update user password
    user = db.query(models.User).filter(models.User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    # Use the imported get_password_hash function
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    # Remove used token
    del reset_tokens[token]
    
    return {"message": "Password has been reset successfully"}