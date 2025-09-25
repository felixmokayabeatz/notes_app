from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import schemas, crud, database, models
from app.auth import create_access_token, get_current_user, get_password_hash
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from datetime import datetime, timezone, timedelta
import secrets, string

router = APIRouter(prefix="/users", tags=["Users"])

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


conf = ConnectionConfig(
    MAIL_USERNAME="youremail@here.com",
    MAIL_PASSWORD="password",
    MAIL_FROM="noreply@domain.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

def generate_reset_token():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

reset_tokens = {}

@router.post("/forgot-password")
async def forgot_password(
    request: dict,
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
        reset_token = generate_reset_token()
        reset_tokens[reset_token] = {
            "user_id": user.id,
            "expires": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        
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
    
    return {"message": "If the email exists, a password reset link has been sent"}

async def send_reset_email(message: MessageSchema):
    fm = FastMail(conf)
    await fm.send_message(message)

@router.post("/reset-password")
async def reset_password(
    request: dict,
    db: Session = Depends(database.get_db)
):
    token = request.get("token")
    new_password = request.get("new_password")
    
    if not token or not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token and new password are required"
        )
    
    if token not in reset_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    token_data = reset_tokens[token]
    
    if datetime.now(timezone.utc) > token_data["expires"]:
        del reset_tokens[token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    user = db.query(models.User).filter(models.User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )

    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    del reset_tokens[token]
    
    return {"message": "Password has been reset successfully"}