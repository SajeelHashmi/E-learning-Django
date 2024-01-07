from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.http import FileResponse
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from Course.models import Course,Assignment,Lecture
from django.http import HttpResponse
from Student.models import Student ,Submissions
from Instructor.models import Instructor
from django.core.files import File
import os
import base64
from django.conf import settings
import time
from .serializers import PostSerializer
from Course.serializers import CourseSerializer,SerializerCourseCard,RegisterCourseSerializer,SubmissionsSerializer,LectureSerializer
from .models import Post
from Notifications.models import Notification



"""each course will have a forum a forum will have many posts and all posts will have a parent id 
the post with parent id null will be a top level post and the rest will be indendet 
functioning 
    return recent posts for a forum and upon scrolling return more the replies will be loaded dynamically
        soo atthe first call we will respond with 10 top level posts with filter parent = null on sub sequent calls we will respond with 10 more
        we still have to fix explore view and its api keep that in mind 
        for replies and not top level post make a view with the same auth as the first view and take a param parent id to get the replies based on that 
        here we will return all the replies instead of pagination """


""" i think this is all done implement this in the front end and then we will move to the last part of adding notifications"""

""" if we have the time and skill we will introduce a websocket here as well"""

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPosts(request,courseId):
    user = request.user
    try:
        course = Course.objects.get(id= courseId)
    except Course.DoesNotExist:
        return Response({"error ": "course doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    allPosts = Post.objects.filter(course=course, parent=None).order_by('-id')
    startNum = request.GET.get('start')
    if not startNum:
        startNum = 0
    endNum = startNum + 10
    posts = allPosts[startNum:endNum]
    try:
        requester = Student.objects.get(user= user)
    except Student.DoesNotExist:
        try:
            requester  = Instructor.objects.get(user =  user)
            if course.instructor != requester:
                return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer = PostSerializer(posts,many = True)
                return Response(serializer.data,status=status.HTTP_200_OK)

        except Instructor.DoesNotExist:
            return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
    if not requester.registeredCourses.filter(id=course.id).exists():
        return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    # return lecture info 
    serializer = PostSerializer(posts,many = True)
    return Response(serializer.data,status=status.HTTP_200_OK)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getReplies(request,courseId,postId):
    user = request.user
    try:
        course = Course.objects.get(id= courseId)
    except Course.DoesNotExist:
        return Response({"error ": "course doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    try:
        parent = Post.objects.get(id=postId)
    except:
        return Response({"error ": "Post doesnot exist"},status=status.HTTP_404_NOT_FOUND)

    replies = Post.objects.filter(course=course, parent=parent)
    
    try:
        requester = Student.objects.get(user= user)
    except Student.DoesNotExist:
        try:
            requester  = Instructor.objects.get(user =  user)
            if course.instructor != requester:
                return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer = PostSerializer(replies,many = True)
                return Response(serializer.data,status=status.HTTP_200_OK)

        except Instructor.DoesNotExist:
            return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
    if not requester.registeredCourses.filter(id=course.id).exists():
        return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    # return lecture info 
    serializer = PostSerializer(replies,many = True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createPost(request,courseId,postId):
    user = request.user
    content = request.data.get('content')
    INS = False
    if not content:
        return Response({"error":"bad request content not provided"},status= status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.objects.get(id= courseId)
    except Course.DoesNotExist:
        return Response({"error ": "course doesnot exist"},status=status.HTTP_404_NOT_FOUND)

    try:
        requester = Student.objects.get(user= user)
    except Student.DoesNotExist:
        try:
            requester  = Instructor.objects.get(user =  user)
            INS = True
            if course.instructor != requester:
                return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
        except Instructor.DoesNotExist:
            return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
    if not requester.registeredCourses.filter(id=course.id).exists():
        return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    regStudents = Student.objects.filter(registeredCourses__in=[course])
    if postId == 0:
        # "create a new post with no parent"
        post = Post.objects.create()
        post.parent =None
        post.content = content
        post.user  = user
        post.course = course
        post.save()
        if INS:
            for std in regStudents:
                notification = Notification.objects.create(user = std.user)
                notification.content = f'Your instructor {requester.name} has posted in the forum for {course.title}'
                notification.associatedLink = f'/forum/{course.id}'
                notification.save()
        else:
            notification = Notification.objects.create(user = course.instructor.user)
            notification.content = f'A Student {requester.name} has posted in the forum for {course.title}'
            notification.associatedLink = f'/forum/{course.id}'
            notification.save()
        serializer =PostSerializer(post,many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    try:
        parent = Post.objects.get(id=postId)
    except:
        return Response({"error ": "parent Post doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    post = Post.objects.create()
    post.parent =parent
    post.content = content
    post.user  = user
    post.course = course
    post.save()
    notification = Notification.objects.create(user = parent.user )
    notification.content = f'{requester.name} has replied to your post in the forum for {course.title}'
    notification.associatedLink = f'/forum/{course.id}'
    notification.save()
    serializer =PostSerializer(post,many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)








