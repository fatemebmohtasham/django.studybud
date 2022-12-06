from django.shortcuts import render,redirect
from django.http import HttpResponse
from.models import  Room,Topic,Messages,User
from django.contrib import messages
from django.contrib.auth  import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from.forms import RoomForm,MessageForm,MyUsercreationForm,UserForm

# Create your views here.

def loginpage(request):
  page='loginpage'
  if request.user.is_authenticated:
    return redirect('home')
  if request.method=='POST':
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
       user=User.objects.get(email=email)
    except:
       messages.error(request,'user does not exist')

    user=authenticate(request,email=email,password=password)
    if user is not None:
      login(request,user) 
      return redirect('home')
    else:
      messages.error(request,'email or password is not correct') 
  context={'page':page}      
  return render(request,'base/login.html',context)

def logoutpage(request):
  logout(request)
  return redirect('home')

def registerpage(request):
  form=MyUsercreationForm()
  if request.method == 'POST':
    form=MyUsercreationForm(request.POST)
    if form.is_valid():
      user=form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request,user)
      return redirect('home')
  context={'form':form}    
  return render(request,'base/login.html',context)    

def home(requst):
  q=requst.GET.get('q') if requst.GET.get('q')!= None else ''
  rooms=Room.objects.filter(
    Q(topic__name__icontains=q)|
    Q(description__icontains=q)|
    Q(name__icontains=q)
    )
  topics=Topic.objects.all()
  message_rooms=Messages.objects.all()
  room_count=rooms.count()
  context={'rooms':rooms , 'topics':topics,'room_count':room_count,'messages_rooms':message_rooms}
  return render(requst,'base/home.html',context)



def room(request,pk):
  room=Room.objects.get(id=pk)
  messagesroom=room.messages_set.all()
  participants=room.participants.all()
  if request.method == 'POST':
    message=Messages.objects.create(
      user=request.user,
      room=room,
      body=request.POST.get('body')
    )
    room.participants.add(request.user)
    return redirect('room',pk=room.id)
  context={'room':room,'messagesroom':messagesroom,'participants':participants}    
  return render(request,'base/room.html',context)


def editemessage(request,pk):
  messages=Messages.objects.get(id=pk)
  message=MessageForm(instance=messages)
  if request.method == 'POST':
    message=MessageForm(request.POST,instance=messages)
    if message.is_valid():
      message.save()
      return redirect('home')
  context={'message':message}
  return render(request,'base/message.html',context)

@login_required(login_url='Login-page')
def createroom(request):
  form=RoomForm()
  topics=Topic.objects.all()
  if request.method=='POST':
    topic_name=request.POST.get('topic')
    topic , created=Topic.objects.get_or_create(name=topic_name)
    Room.objects.create(
      host=request.user,
      topic=topic,
      name=request.POST.get('name'),
      description=request.POST.get('description'),
    )
    return redirect('home')
  context={'form':form,'topics':topics}
  return render(request,'base/room-form.html',context)

@login_required(login_url='Login-page')
def updateroom(request,pk):
  room=Room.objects.get(id=pk)
  topics=Topic.objects.all()
  form=RoomForm(instance=room)
  if request.user != room.host:
    return HttpResponse('you are not allowed')
  if request.method=='POST':
    topic_name=request.POST.get('topic')
    topic , created=Topic.objects.get_or_create(name=topic_name)
    room.name= request.POST.get('name')
    room.description= request.POST.get('description')
    room.topic=topic
    return redirect('home')
  context={'form':form,'topics':topics}
  return render(request,'base/room-form.html',context)

@login_required(login_url='Login-page')
def deleteroom(request,pk):
  room=Room.objects.get(id=pk)
  if request.method=='POST':
     room.delete()
     return redirect('home')
  return render(request,'base/delete.html',{'obj':room})  


@login_required(login_url='Login-page')
def deletemessage(request,pk):
  message=Messages.objects.get(id=pk)
  if request.method=='POST':
     message.delete()
     return redirect('home')
  return render(request,'base/delete.html',{'obj':message})  


def userprofile(request,pk):
  user=User.objects.get(id=pk)
  rooms=user.room_set.all()
  messages_rooms=user.messages_set.all()
  topics=Topic.objects.all()
  context={'user':user,'rooms':rooms,'topics':topics,'messages_rooms':messages_rooms}
  return render(request,'base/profile.html',context)  


@login_required(login_url='Login-page')
def edituser(request):
  user=request.user
  form=UserForm(instance=user)
  if request.method == 'POST':
    form=UserForm(request.POST,request.FILES ,instance=user)
    if form.is_valid:
      form.save()
    return redirect('userprofile',pk=user.id)  
  context={'form':form}
  return render(request,'base/edit-user.html',context)



def topicpag(request):
  q=request.GET.get('q') if request.GET.get('q')!= None else ''
  topics=Topic.objects.filter(name__icontains=q)
  context={'topics':topics}
  return render(request,'base/topics.html',context)

def activitypag(request):
  messages_rooms=Messages.objects.all()
  context={'messages_rooms':messages_rooms}
  return render(request,'base/activity.html',context)  