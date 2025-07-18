from django.urls import path
from . import views

app_name = 'landing' 

urlpatterns = [
    path("", views.home, name="home"),
    path("teachers/<int:pk>", views.teacher, name="teacher"),
    path("teachers/<int:teacher_id>/review/", views.add_review, name="add_review"),
    path("admin/delete-review/<int:review_id>/", views.delete_review, name="delete_review"),
    path("admin/approve-teacher/<int:pk>/", views.approve_teacher, name="approve_teacher"),
    path("admin/delete-teacher/<int:pk>/", views.delete_teacher, name="delete_teacher"),
    path("admin/deactivate-teacher/<int:pk>/", views.deactivate_teacher, name="deactivate_teacher"),
]