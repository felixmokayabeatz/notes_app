from django.urls import path
from .views import register_view, login_view, notes_list, create_note, edit_note, share_note, view_shared_note, landing_page, forgot_password_page, reset_password_page
from .generate_api_key import generate_api_key, api_key_page

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("notes/", notes_list, name="notes_list"),
    path("notes/new/", create_note, name="create_note"),
    path("notes/<int:note_id>/edit/", edit_note, name="edit_note"),
    path("notes/<int:note_id>/share/", share_note, name="share_note"),
    path("notes/shared/<str:share_id>/", view_shared_note, name="view_shared_note"),
    path("api-key/", api_key_page, name="api_key_page"),
    path("api-key/generate/", generate_api_key, name="generate_api_key"),
    path("forgot-password/", forgot_password_page, name="forgot_password"),
    path("reset-password/", reset_password_page, name="reset_password"),


]
