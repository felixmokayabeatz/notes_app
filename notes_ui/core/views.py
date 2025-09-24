import requests
from django.shortcuts import render, redirect
from django.conf import settings

API_BASE = "http://127.0.0.1:8000"  # your FastAPI backend

# Simple session-based auth
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        res = requests.post(f"{API_BASE}/auth/login", json={"username": username, "password": password})
        if res.status_code == 200:
            request.session["token"] = res.json()["access_token"]
            return redirect("notes_list")
    return render(request, "login.html")

def notes_list(request):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    res = requests.get(f"{API_BASE}/notes", headers=headers)
    notes = res.json() if res.status_code == 200 else []
    return render(request, "notes.html", {"notes": notes})

def create_note(request):
    token = request.session.get("token")
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        headers = {"Authorization": f"Bearer {token}"}
        requests.post(f"{API_BASE}/notes", json={"title": title, "content": content}, headers=headers)
        return redirect("notes_list")
    return render(request, "create_note.html")
