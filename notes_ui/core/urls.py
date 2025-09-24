from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("notes/", views.notes_list, name="notes_list"),
    path("notes/new/", views.create_note, name="create_note"),
]
