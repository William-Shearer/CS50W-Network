from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.register, name = "register"),
    path("changepassword", views.change_password, name = "changepassword"),
    path("editprofile", views.edit_profile, name = "editprofile"),
    path("viewprofile/<int:user_id>", views.view_profile, name = "viewprofile"),
    path("like/<int:post_id>", views.like_post, name = "like"),
    path("viewprofile/like/<int:post_id>", views.like_post, name = "vplike"),
    path("getlikes/<int:post_id>", views.get_likes, name = "getlikes"),
    path("viewprofile/getlikes/<int:post_id>", views.get_likes, name = "vpgetlikes"),
    path("putedit/<int:post_id>", views.put_edit, name = "putedit"),
    path("viewprofile/putedit/<int:post_id>", views.put_edit, name = "vpputedit"),
    path("geteditdate/<int:post_id>", views.get_editdate, name = "geteditdate"),
    path("viewprofile/geteditdate/<int:post_id>", views.get_editdate, name = "vpgeteditdate"),
    path("viewprofile/putfollow/<int:member_id>", views.put_follow, name = "putfollow"),
    path("viewprofile/getfollow/<int:member_id>", views.get_follow, name = "getfollow"),
    path("userfollowsposts", views.user_follows_posts, name = "userfollowsposts"),
    path("viewprofile/updatefollowed/<int:member_id>", views.update_followed, name = "updatefollowed")
]
