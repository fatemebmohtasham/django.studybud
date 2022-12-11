from rest_framework.response import Response
from . serializers import RoomSerializer
from rest_framework.decorators import api_view
from base.models import Room



@api_view(["GET"])
def get_rooms(request):
  if request.method == "GET":
    queryset=Room.objects.all()
    serializer=RoomSerializer(queryset,many=True)
    return Response (serializer.data)

@api_view(["GET"])
def get_room(request,pk):
  if request.method == "GET":
    queryset=Room.objects.get(id=pk)
    serializer=RoomSerializer(queryset,many=False)
    return Response (serializer.data)