from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Notification
from rest_framework.exceptions import AuthenticationFailed
from Student.serializers import userSerializer


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(user = user).order_by('read').order_by('-id')
    data = []
    for notification in notifications:
        obj = {}
        obj['content'] = notification.content
        obj['read'] = notification.read
        obj['link'] =notification.associatedLink
        obj['id'] = notification.id
        data.append(obj)

    return Response({'data':data},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def count(request):
    user = request.user
    return Response({"count":Notification.objects.filter(user = user,read = False).count()},status=status.HTTP_200_OK)
  


                

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def markAsRead(request,id):
    user = request.user
    try:
        notification = Notification.objects.get(id = id)
    except:
        return Response({'error':'notifaction does not exist'},status=status.HTTP_404_NOT_FOUND)
    if notification.user == user:
        notification.read = True
        notification.save()
        return Response({'success':"notification markAsRead as read"},status=status.HTTP_200_OK)
    return Response({'error':'unauthorized access'},status=status.HTTP_401_UNAUTHORIZED)




@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteNotification(request):
    user = request.user
    try:
        notification = Notification.objects.get(id = id)
    except:
        return Response({'error':'notifaction does not exist'},status=status.HTTP_404_NOT_FOUND)
    if notification.user == user:
        notification.delete()
        return Response({'success':"notification deleted"},status=status.HTTP_200_OK)
    return Response({'error':'unauthorized access'},status=status.HTTP_401_UNAUTHORIZED)

