from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("notes/", views.notes_list, name="notes_list"),
    path("notes/new/", views.create_note, name="create_note"),
    path("notes/<int:note_id>/edit/", views.edit_note, name="edit_note"),
    path("notes/<int:note_id>/share/", views.share_note, name="share_note"),
    path("notes/shared/<str:share_id>/", views.view_shared_note, name="view_shared_note"),
]
