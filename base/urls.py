from django.urls import path
from.import views
urlpatterns=[
  path('loginpage/',views.loginpage,name="Login-page"),
  path('logoutpage/',views.logoutpage,name="Logout-page"),
  path('registerpage/',views.registerpage,name="register-page"),
  path('',views.home,name="home"),
  path('room_page/<str:pk>',views.room,name="room"),
  path('create-room/',views.createroom,name="create-room"),
  path('update-room/<str:pk>/',views.updateroom,name="update-room"),
  path('delete-room/<str:pk>/',views.deleteroom,name="delete-room"),
  path('delete-message/<str:pk>/',views.deletemessage,name="delete-message"),
  path('edite-message/<str:pk>/',views.editemessage,name="edite-message"),
  path('userprofile/<str:pk>/',views.userprofile,name="userprofile"),
  path('edituser/',views.edituser,name="edituser"),
  path('topicpage/',views.topicpag,name="topics"),
  path('activitypage/',views.activitypag,name="activity"),
]