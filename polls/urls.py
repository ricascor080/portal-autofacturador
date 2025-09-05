from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "polls"

urlpatterns = [
    # Tutorial original
    path("", views.index, name="index"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # Autenticación
    path("login/", views.user_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", LogoutView.as_view(next_page="polls:login"), name="logout"),
    path("register/", views.register, name="register"),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    #admin
    path("add_question/", views.add_question, name="add_question"),
    path("add_choice/", views.add_choice, name="add_choice"),
    path("export_csv/", views.export_csv, name="export_csv"),
]
