import requests
from django.shortcuts import render, redirect

API_BASE = "http://127.0.0.1:8000"  # FastAPI backend

# ----------------- Auth Views -----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        res = requests.post(
            f"{API_BASE}/users/login",
            data={"username": username, "password": password},  # OAuth2 expects form-data
        )

        if res.status_code == 200:
            request.session["token"] = res.json()["access_token"]
            return redirect("notes_list")
        else:
            error = res.json().get("detail", "Invalid login")
            return render(request, "login.html", {"error": error})

    return render(request, "login.html")


def register_view(request):
    error = None
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        res = requests.post(
            f"{API_BASE}/users/register",
            json={"email": email, "password": password},
        )

        if res.status_code == 200:
            return redirect("login")
        else:
            error = res.json().get("detail", "Registration failed")

    return render(request, "register.html", {"error": error})


# ----------------- Notes Views -----------------
def notes_list(request):
    token = request.session.get("token")
    if not token:
        return redirect("login")  # No token, force login

    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_BASE}/notes/", headers=headers)

    if res.status_code == 401:
        # Token expired or invalid -> clear session and force re-login
        request.session.flush()
        return redirect("login")

    notes = res.json() if res.status_code == 200 else []
    return render(request, "notes.html", {"notes": notes})



def create_note(request):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        requests.post(
            f"{API_BASE}/notes/",
            json={"title": title, "content": content},
            headers=headers,
        )
        return redirect("notes_list")

    return render(request, "create_note.html")


def edit_note(request, note_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        shared = "shared" in request.POST  # checkbox → bool

        requests.put(
            f"{API_BASE}/notes/{note_id}",
            json={"title": title, "content": content, "shared": shared},
            headers=headers,
        )
        return redirect("notes_list")


    # Pre-fill the form with existing data
    res = requests.get(f"{API_BASE}/notes/{note_id}", headers=headers)
    note = res.json() if res.status_code == 200 else {}

    return render(request, "edit_note.html", {"note": note})


def delete_note(request, note_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    requests.delete(f"{API_BASE}/notes/{note_id}", headers=headers)
    return redirect("notes_list")

# views.py

def share_note(request, note_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # Fetch the note to get share_id
    res = requests.get(f"{API_BASE}/notes/{note_id}", headers=headers)
    if res.status_code != 200:
        return redirect("notes_list")

    note = res.json()
    if not note.get("shared") or not note.get("share_id"):
        # force share first if not already shared
        return redirect("edit_note", note_id=note_id)

    # Instead of redirecting to FastAPI, fetch the shared note content
    shared_res = requests.get(f"{API_BASE}/notes/shared/{note['share_id']}")
    if shared_res.status_code != 200:
        return redirect("notes_list")

    shared_note = shared_res.json()

    # Render in template
    return render(request, "shared_note.html", {"note": shared_note})


