from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    path("practice/<int:section_id>/", views.practice_view, name="practice"),
    path("mock-test/", views.mock_test_view, name="mock_test"),
    path("upload-jd/", views.upload_jd_view, name="upload_jd"),
    path("jd-mock-test/", views.jd_mock_test_view, name="jd_mock_test"),

]

