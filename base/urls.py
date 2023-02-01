from django.urls import path

from base import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_page, name="register"),

    path("", views.home_page, name="home"),
    path("room/<str:pk>", views.room_page, name="room"),
    path("profile/<str:pk>", views.user_profile, name="user-profile"),

    path("create-room/", views.create_room, name="create-room"),
    path("update-room/<str:pk>", views.update_room, name="update-room"),
    path("delete-room/<str:pk>", views.delete_room, name="delete-room"),

    path("delete-message/<str:pk>", views.delete_message, name="delete-message"),

    path("update-user/", views.update_user, name="update-user"),
    path("reset-avatar/", views.reset_avatar, name="reset-avatar"),

    path("topics/", views.topics_page, name="topics"),
    path("activity/", views.activity_page, name="activity"),
]
