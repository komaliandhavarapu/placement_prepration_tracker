from django.urls import path
from . import views
from . import coding_views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("practice/<int:section_id>/", views.practice_view, name="practice"),
    path("mock-test/", views.mock_test_view, name="mock_test"),
    path("upload-jd/", views.upload_jd_view, name="upload_jd"),
    path("jd-mock-test/", views.jd_mock_test_view, name="jd_mock_test"),
    path("mock-interview/", views.mock_interview_view, name="mock_interview"),
    path("mock-interview-result/", views.mock_interview_result_view, name="mock_interview_result"),
    path("coding/", coding_views.coding_practice_view, name="coding_practice"),
    path("coding/execute/", coding_views.coding_execute_view, name="coding_execute"),
    path("coding/result/", coding_views.coding_result_view, name="coding_result"),
]

