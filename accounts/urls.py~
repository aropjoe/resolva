from . import views
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path('mediator/details/<int:id>/', views.view_mediator, name="mediator"),
    path("account/details/<int:id>/", views.view_account, name="account"),
    path("add-qualification/", views.add_qualification, name="add_qualification"),
    path("add-affiliation/", views.add_affiliation, name="add_affiliation"),
    path("mediator/create/", views.create_mediator, name="create_mediator"),
    path("account/create/", views.create_account, name="create_account"),
    path("login/", views.login, name="login"),
]
