from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from Course.models import Course,Assignment,Lecture
from django.http import HttpResponse
from .models import Instructor,Application
from Student.models import Student,Submissions

from django.conf import settings
from .serializers import instructorSerializer
from Course.serializers import CourseSerializer,SerializerCourseCard
from .serializers import YourCourseSerializer
from django.http import FileResponse
from Notifications.models import Notification
import os
from IlmGhar.emailAlerts import applicationRecieved,applicationRecievedAdmin


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def instructorsCourses(request):
    INS = request.GET.get('ins')
    if not INS:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    try:
        instructor = Instructor.objects.get(user = user)
    except:
        return Response({"error":"Instructor does not exist"},status=status.HTTP_401_UNAUTHORIZED)
    courses = Course.objects.filter(instructor = instructor)
    serializer = SerializerCourseCard(courses,many= True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getCourseDate(request):
    INS = request.GET.get('ins')
    print(INS)
    if not INS:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)
    id = request.GET.get('id')
    if id is None:
        return Response({"error":"Provide Id for course"},status=status.HTTP_400_BAD_REQUEST)
    user = request.user
    try:
        instructor = Instructor.objects.get(user = user)
    except Instructor.DoesNotExist:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)
    try:
        course = Course.objects.get(id = id)
    except Course.DoesNotExist:
        return Response({"error":"course doesnot exist"},status=status.HTTP_404_NOT_FOUND)
  
    if course.instructor == instructor:
        serializer = YourCourseSerializer(course,many = False)
 
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateBio(request):
    INS = request.GET.get('ins')
    if not INS:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)
    bio = request.data.get('bio')
    if not bio:
        return Response({"error":"expecting bio got none"},status=status.HTTP_400_BAD_REQUEST)
    user = request.user
    try:
        instructor = Instructor.objects.get(user = user)
    except Instructor.DoesNotExist:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)
    instructor.bio = bio
    instructor.save()
    return Response({"success":"bio updated successfully"},status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def instructorInfo(request):
    print("request recieved")
    INS = request.GET.get('ins')
    if not INS:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    try:
        instructor = Instructor.objects.get(user = user)
    except:
        return Response({"error":"Instructor does not exist"},status=status.HTTP_401_UNAUTHORIZED)
    serializer = instructorSerializer(instructor,many= False)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadSubmission(request,lectureId):
    INS = request.GET.get('ins')
    studentId = request.GET.get('id')
    if not INS and not studentId:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    try:
        instructor = Instructor.objects.get(user = user)
    except:
        return Response({"error":"Instructor does not exist"},status=status.HTTP_401_UNAUTHORIZED)
    try:
        student = Student.objects.get(id=studentId)
    except Student.DoesNotExist:
        return Response({"error":"student does not exist"},status=status.HTTP_401_UNAUTHORIZED)
    try:
        lecture = Lecture.objects.get(id = lectureId)
        assignment = Assignment.objects.get(lecture=lecture)
        submission = Submissions.objects.get(assignment = assignment,student = student)
    except Lecture.DoesNotExist:
        return Response({'error': 'Lecture not found'}, status=status.HTTP_404_NOT_FOUND)
    except Submissions.DoesNotExist:
        return Response({'error': 'not submitted yet'}, status=status.HTTP_404_NOT_FOUND)
    
    file_path = os.path.join(settings.MEDIA_ROOT,  str(submission.submission))
    print(file_path)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        return response
    else:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)






@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def checkSubmission(request,lectureId):
    INS = request.GET.get('ins')
    studentId = request.GET.get('id')
    if not INS and not studentId:
        return Response({"error":"not authorized"},status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    try:
        instructor = Instructor.objects.get(user = user)
    except:
        return Response({"error":"Instructor does not exist"},status=status.HTTP_401_UNAUTHORIZED)
    try:
        student = Student.objects.get(id=studentId)
    except Student.DoesNotExist:
        return Response({"error":"student does not exist"},status=status.HTTP_401_UNAUTHORIZED)
    try:
        lecture = Lecture.objects.get(id = lectureId)
        assignment = Assignment.objects.get(lecture=lecture)
        submission = Submissions.objects.get(assignment = assignment,student = student)
    except Lecture.DoesNotExist:
        return Response({'error': 'Lecture not found'}, status=status.HTTP_404_NOT_FOUND)
    except Submissions.DoesNotExist:
        return Response({'error': 'not submitted yet'}, status=status.HTTP_404_NOT_FOUND)
    if submission.checked:
        return Response({'error': 'submission already checked'}, status=status.HTTP_412_PRECONDITION_FAILED)
    marks = request.data.get('marks')
    remarks = request.data.get('remarks')
    if marks and remarks:
        submission.marksObt = marks
        submission.remarks = remarks
        submission.checked = True
        notification = Notification.objects.create(user =student.user)
        notification.content = f"Your assignment {assignment.title} of {assignment.lecture.course.title}  has been checked. You got {submission.marksObt} out of {assignment.marks} marks"
        notification.associatedLink = f'/registered/{assignment.lecture.course.id}'
        notification.save()
        submission.save()
        return Response({"success":"submission checked successfully"})
    return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def newApplication(request):
    firstName = request.data.get('firstName')
    lastName = request.data.get('lastName')
    description = request.data.get('description')
    email = request.data.get('email')
    app = Application.objects.create(firstName = firstName,lastName = lastName,description = description,email = email)
    applicationRecievedAdmin(email,lastName)
    applicationRecieved(email=email,name=lastName)
    return Response({"success":"Application Recieved"})
