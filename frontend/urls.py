from django.urls import path

from frontend.views import home, auth_login, auth_logout, author_register, member_register, profile

urlpatterns = [
    path('', home, name='home'),
    path('login',auth_login, name='login'),
    path('logout',auth_logout,name='logout'),
    path('author_register',author_register,name='author_register'),
    path('member_register',member_register,name='member_register'),
    path('profile',profile, name='profile'),
]