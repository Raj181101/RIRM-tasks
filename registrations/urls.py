from django.conf.urls import url
from django.urls import include, path
from .views import *

urlpatterns = [
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path("logout", logout_request, name= "logout"),
    path("reset_password", reset_password, name= "reset_password"),
    
    ### Student Info Urls
    url(r'^$', index, name='index'),
    url(r'^students$', display_students, name="display_students"),

    url(r'^add_student$', add_student, name="add_student"),

    url(r'^students/edit_item/(?P<pk>\d+)$', edit_student, name="edit_student"),

    url(r'^students/delete/(?P<pk>\d+)$', delete_student, name="delete_student"),
    
    ### Student Academic Urls
    url(r'^student_academics/(?P<pk>\d+)$', display_student_academic, name="student_academics"),

    url(r'^add_student_academic', add_student_academic, name="add_student_academic"),

    url(r'^students/edit_academics/(?P<pk>\d+)$', edit_academics, name="edit_academics"),

    url(r'^students/delete_academics/(?P<pk>\d+)$', delete_academics, name="delete_academics"),
    
    ## Extracting Links based on website url
    path("extract_links", extract_links, name= "extract_links"),

]