from django.urls import path
from .views import RegisterView ,LoginView , UserView, LogoutView, UserList ,UserDetail,StudentDetail,StudentList,TeacherList,TeacherDetail

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('users', UserList.as_view()),
    path('users/<int:pk>',UserDetail.as_view()),
    path('students',StudentList.as_view()),
    path('students/<int:pk>',StudentDetail.as_view()),
    path('teachers',TeacherList.as_view()),
    path('teachers/<int:pk>',TeacherDetail.as_view()),





]
