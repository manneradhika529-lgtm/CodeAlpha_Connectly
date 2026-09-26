from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='comment'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('profile/', views.profile, name='profile'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('search/', views.search_users, name='search_users'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('notifications/', views.notifications, name='notifications'),





]
