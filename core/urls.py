from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path("session/<id>/", views.view_session, name="session"),
    path("create-session/<id>/", views.create_session, name="create_session"),
    path("dispute/<id>/", views.view_dispute, name="dispute"),
    path("delete-dispute/", views.delete_dispute, name="delete_dispute"),
    path("create-dispute/", views.create_dispute, name="create_dispute"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("disputes/", views.dashboard, name="disputes"),
    path("", views.landing, name="landing"),
    path("new-message/", views.new_message, name="new_message"),
    path("file-upload/<id>/", views.upload_file, name="upload"),
]
