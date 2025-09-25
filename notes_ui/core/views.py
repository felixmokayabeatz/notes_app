import requests
from django.shortcuts import render, redirect
from django.urls import reverse

API_BASE = "http://127.0.0.1:8000"


def landing_page(request):
    """Modern landing page with animations"""
    return render(request, 'landing.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        res = requests.post(
            f"{API_BASE}/users/login",
            data={"username": username, "password": password},
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

def notes_list(request):
    token = request.session.get("token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_BASE}/notes/", headers=headers)

    if res.status_code == 401:
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
        shared = "shared" in request.POST

        requests.put(
            f"{API_BASE}/notes/{note_id}",
            json={"title": title, "content": content, "shared": shared},
            headers=headers,
        )
        return redirect("notes_list")

    res = requests.get(f"{API_BASE}/notes/{note_id}", headers=headers)
    note = res.json() if res.status_code == 200 else {}

    return render(request, "edit_note.html", {"note": note})


def delete_note(request, note_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    requests.delete(f"{API_BASE}/notes/{note_id}", headers=headers)
    return redirect("notes_list")


def share_note(request, note_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    res = requests.get(f"{API_BASE}/notes/{note_id}", headers=headers)
    if res.status_code != 200:
        return redirect("notes_list")

    note = res.json()
    if not note.get("shared") or not note.get("share_id"):
        return redirect("edit_note", note_id=note_id)

    public_link = request.build_absolute_uri(
        reverse("view_shared_note", args=[note["share_id"]])
    )

    return render(request, "share_link.html", {"note": note, "public_link": public_link})


def view_shared_note(request, share_id):
    res = requests.get(f"{API_BASE}/notes/shared/{share_id}")
    if res.status_code != 200:
        return render(request, "shared_note.html", {"note": None, "error": "Note not found, or the Owner stoped sharing"})

    note = res.json()
    return render(request, "shared_note.html", {"note": note})


from django.shortcuts import render

def forgot_password_page(request):
    return render(request, "forgot_password.html")

def reset_password_page(request):
    token = request.GET.get("token")
    return render(request, "reset_password.html", {"token": token})
