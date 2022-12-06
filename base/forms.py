from django.forms import ModelForm
from.models import Room,Messages,User
from django.contrib.auth.forms import UserCreationForm

class MyUsercreationForm(UserCreationForm):
  class Meta:
    model=User
    fields=['name','username','avatar','email','password1','password2']  


class RoomForm(ModelForm):
  class Meta:
    model=Room
    fields='__all__'
    exclude=['host','participants']

class MessageForm(ModelForm):
  class Meta:
    model=Messages
    fields='__all__'  

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']