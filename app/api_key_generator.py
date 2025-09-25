import secrets, bcrypt, requests
from sqlalchemy.orm import Session
from app import models, database
from django.http import JsonResponse

def generate_api_key_string() -> str:
    return secrets.token_hex(32)

def hash_api_key(api_key: str) -> str:
    return bcrypt.hashpw(api_key.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def save_api_key_to_db(api_key: str, owner="felix"):
    db: Session = database.SessionLocal()
    try:
        key_hash = hash_api_key(api_key)
        db_key = models.ApiKey(key_hash=key_hash, owner=owner)
        db.add(db_key)
        db.commit()
        return key_hash
    finally:
        db.close()

def verify_api_key(api_key: str) -> bool:
    db: Session = database.SessionLocal()
    try:
        keys = db.query(models.ApiKey).all()
        for stored in keys:
            if bcrypt.checkpw(api_key.encode("utf-8"), stored.key_hash.encode("utf-8")):
                return True
        return False
    finally:
        db.close()

def create_api_key_view(request):
    if request.method == "POST":
        try:
            resp = requests.post("http://127.0.0.1:8000/generate-api-key")
            return JsonResponse(resp.json(), safe=False, status=resp.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
