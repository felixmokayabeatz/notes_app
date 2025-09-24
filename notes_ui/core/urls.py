from django.urls import path
from .views import register_view, login_view, notes_list, create_note, edit_note, share_note, view_shared_note

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("notes/", notes_list, name="notes_list"),
    path("notes/new/", create_note, name="create_note"),
    path("notes/<int:note_id>/edit/", edit_note, name="edit_note"),
    path("notes/<int:note_id>/share/", share_note, name="share_note"),
    path("notes/shared/<str:share_id>/", view_shared_note, name="view_shared_note"),
]
