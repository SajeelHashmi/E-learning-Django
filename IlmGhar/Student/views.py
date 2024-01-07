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
from .models import Student ,Submissions
from Instructor.models import Instructor
from Notifications.models import Notification

from django.core.files import File
import os
import base64
from django.conf import settings
import time
from .serializers import studentSerializer
from django.db.models import Q
from Course.serializers import CourseSerializer,SerializerCourseCard,RegisterCourseSerializer,SubmissionsSerializer,LectureSerializer
from IlmGhar.emailAlerts import enrolledInCourseIns,enrolledInCourse
# Create your views here.

"""customizing the three get views for assignments notes and submissions 
instead of using file name and pregenerated links we will use lecture id for assignments and notes
and submission id for submissions"""


#notes and assignmnets
"""extract user or instructor then check if that user has enrolled in that lecture if yes send back notes"""


#submissions
"""check if user is student if yes check if the student in the submission id provided is the same if yes send back
if user is instructor extract assignment the from assignment extract lecture and from there get instructor if these 2 are the same return the file
"""



"""main functionality that is left is the play lecture authentication and then moving forward adding of forums and notifications
apart from that this module could be considered as complete after this we will jump in the instructor model and define some views there"""

"""creation of forum app and notifications app 
forum app to be created next and lastly the notification app
forum app will not require a lot of integration but the notification app 
after all this work on finalizing your design and give flutter a go in the last 2 3 days if you have any 
because of the backend api being done it wont take a lot of effort all the focus will be on design 
"""

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getLectureInfo(request,courseId,lectureId):
    user = request.user
    user = request.user
    try:
        course = Course.objects.get(id= courseId)
    except Course.DoesNotExist:
        return Response({"error ": "course doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    try:
        lecture = Lecture.objects.get(id = lectureId)
    except Lecture.DoesNotExist:
        return Response({"error ": "lecture doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    try:
        requester = Student.objects.get(user= user)
    except Student.DoesNotExist:
        try:
            requester  = Instructor.objects.get(user =  user)
            if course.instructor != requester:
                return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer  = LectureSerializer(lecture,many = False)
                return Response(serializer.data,status=status.HTTP_200_OK)

        except Instructor.DoesNotExist:
            return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
    if not requester.registeredCourses.filter(id=course.id).exists():
        return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    # return lecture info 
    serializer  = LectureSerializer(lecture,many = False)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def registeredCourses(request):
    print('here')
    user = request.user
    try:
        student = Student.objects.get(user = user)
    except:
        return Response({"error":"Student does not exist"},status=status.HTTP_400_BAD_REQUEST)
    courses = student.registeredCourses.all()
    serializer = SerializerCourseCard(courses,many= True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def suggestedCourse(request):
    user = request.user
    try:
        student = Student.objects.get(user = user)
    except:
        return Response({"error":"Student does not exist"},status=status.HTTP_400_BAD_REQUEST)
    courses = student.registeredCourses.all()
    if len(courses) == 0:
        suggested = Course.objects.all()
        suggested = suggested.exclude(id__in=[course.id for course in courses])
        suggested = suggested[:3]
        serializer = SerializerCourseCard(suggested,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    data = {
        'subjects':set(),
        'languages':set(),
        'tags':set(),

    }
    for course in courses:
        data['subjects'].add(course.subject)
        data['languages'].add(course.language.name)
        for tag in course.tags.all():
            data['tags'].add(tag.name)

    # now using this data filter
    query = Q(language__name__in=data['languages']) | Q(tags__name__in=data['tags']) | Q(subject__name__in=data['subjects'])
    suggested = Course.objects.filter(query).distinct()
    print(suggested)

    suggested = suggested.exclude(id__in=[course.id for course in courses])

    suggested = suggested[:3]
    if len(suggested) == 0:
        suggested = Course.objects.all()
        suggested = suggested.exclude(id__in=[course.id for course in courses])
        suggested = suggested[:3]
        serializer = SerializerCourseCard(suggested,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = SerializerCourseCard(suggested, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def submitAssingment(request ,assingmentId):
    user = request.user
    file = request.FILES['submission']
    if not file:
        return Response({"error":"Please upload submission"},status=status.HTTP_400_BAD_REQUEST)
    try:
        student = Student.objects.get(user = user)
    except:
        return Response({"error":"Student does not exist"},status=status.HTTP_404_NOT_FOUND)
    try:
        assignment = Assignment.objects.get(id = assingmentId)
    except:
        return Response({"error":"Assignment does not exist"},status=status.HTTP_404_NOT_FOUND)    
    try:
        submission = Submissions.objects.get(assignment = assignment,student =student)
        return Response({"message":{"assignment already submitted"}},status=status.HTTP_200_OK)
    except:
        submission = Submissions.objects.create(student = student,assignment = assignment,submission = file)
        submission.save()
        notification = Notification.objects.create(user =  assignment.lecture.course.instructor.user)
        notification.content = f"{student.name} has uploaded submission for assignment {assignment.lecture.number} of course {assignment.lecture.course.title}"
        notification.associatedLink  = f'/yourcourse/{assignment.lecture.course.id}'
        notification.save()
        return Response({"message":{"assignment submitted successfully"}},status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def studentInfo(request):
    user = request.user
    try:
        student = Student.objects.get(user = user)
    except:
        return Response({"error":"Student does not exist"},status=status.HTTP_400_BAD_REQUEST)
    serializer = studentSerializer(student,many = False)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view([ 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def registernNewCourse(request,id):
    user = request.user
    if id is None:
        return Response({"error":"Provide Id for course"},status=status.HTTP_400_BAD_REQUEST)
    print(id)

    try:
        course = Course.objects.get(id = id) 
    except:
        return Response({"error":"course does not exist"},status=status.HTTP_400_BAD_REQUEST)
    try:
        student = Student.objects.get(user = user) 
    except:
        return Response({"error":"Student does not exist"},status=status.HTTP_400_BAD_REQUEST)
    student.registeredCourses.add(course)
    notificationUser = course.instructor.user
    notification  = Notification.objects.create(user = notificationUser)
    notification.associatedLink = f'/yourcourse/{course.id}'
    notification.content = f'A new Student {student.name} has registered in your course {course.title}'
    notification.save()
    student.save()
    enrolledInCourse(email=student.user.email,name=student.name,course=course.title)
    enrolledInCourseIns(email=course.instructor.user.email,name=course.instructor.name,course=course.title)
    return Response({"Success": "Course registered succcessfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getRegisteredCourse(request):
    user = request.user
    print('here')
    id = request.GET.get('id')
    if id is None:
        return Response({"error":"Provide Id for course"},status=status.HTTP_400_BAD_REQUEST)
    try:
        student = Student.objects.get(user = user)
    except:
        return Response({"error":"Student does not exist"},status=status.HTTP_400_BAD_REQUEST)

    try:
        course = student.registeredCourses.get(id=id)
    except:
        return Response({"error":"This course has not been registered by student or does not exist"},status=status.HTTP_400_BAD_REQUEST)
    serilizer = RegisterCourseSerializer(course)
    for lecture in serilizer.data['lectures']:
        assignmentId = lecture['assignment']['id']
        assignment = Assignment.objects.get(id = assignmentId)
        try:
            submission = Submissions.objects.get(assignment = assignment, student = student)
        except:
            lecture['assignment']['submission'] = False
            continue
        lecture['assignment']['submission'] = SubmissionsSerializer(submission).data
    return Response(serilizer.data)







# working use same template for the rest of the get files views
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def downloadAssignment(request,courseId):
    lectureId = request.GET.get('id')
    print("downloading assignment")
    if not lectureId:
        return Response({"error":"bad request lecture id not provided"},status= status.HTTP_400_BAD_REQUEST)
    user = request.user
    print(user)
    try:
        course = Course.objects.get(id = courseId)
    except Course.DoesNotExist:
        return Response({"error": "course not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        student = Student.objects.get(user=user)
        if not student.registeredCourses.filter(id=course.id).exists():
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    except Student.DoesNotExist:
        try:
            instructor = Instructor.objects.get(user=user)
            if course.instructor != instructor:
                return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)                
        except Instructor.DoesNotExist:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
    # Fetch the assignment using lectureId
    try:
        lecture = Lecture.objects.get(id = lectureId,course = course)
        assignment = Assignment.objects.get(lecture=lecture)
    except Lecture.DoesNotExist:
        return Response({'error': 'Lecture not found'}, status=status.HTTP_404_NOT_FOUND)

    file_path = os.path.join(settings.MEDIA_ROOT,  str(assignment.file))
    print(file_path)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        print(response.headers)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'   
        return response
    else:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    


#working
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def downloadSubmission(request, courseId):
    lectureId = request.GET.get('id')
    print(lectureId)
    if not lectureId:
        return Response({"error":"bad request lecture id not provided"},status= status.HTTP_400_BAD_REQUEST)
    user = request.user
    print(user)
    try:
        course = Course.objects.get(id = courseId)
    except Course.DoesNotExist:
        return Response({"error": "course not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        student = Student.objects.get(user=user)
        if not student.registeredCourses.filter(id=course.id).exists():
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    except Student.DoesNotExist:
        try:
            instructor = Instructor.objects.get(user=user)
            if course.instructor != instructor:
                return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)                
        except Instructor.DoesNotExist:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
    # Fetch the submission using lectureId
    try:
        lecture = Lecture.objects.get(id = lectureId,course = course)
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




#working
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def downloadNotes(request, courseId):
    lectureId = request.GET.get('id')
    print(lectureId)
    if not lectureId:
        return Response({"error":"bad request lecture id not provided"},status= status.HTTP_400_BAD_REQUEST)
    user = request.user
    print(user)
    try:
        course = Course.objects.get(id = courseId)
    except Course.DoesNotExist:
        return Response({"error": "course not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        student = Student.objects.get(user=user)
        if not student.registeredCourses.filter(id=course.id).exists():
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    except Student.DoesNotExist:
        try:
            instructor = Instructor.objects.get(user=user)
            if course.instructor != instructor:
                return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)                
        except Instructor.DoesNotExist:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
    try:
        lecture = Lecture.objects.get(id = lectureId,course = course)

    except Lecture.DoesNotExist:
        return Response({'error': 'Lecture not found'}, status=status.HTTP_404_NOT_FOUND)
    
    file_path = os.path.join(settings.MEDIA_ROOT,  str(lecture.notes))
    print(file_path)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        return response
    else:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

# add authentication to returnm3u8 and play lecture view 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def returnM3U8(request,courseId ,lectureId):

    user = request.user
    print(user)

    try:
        course = Course.objects.get(id= courseId)
    except Course.DoesNotExist:
        return Response({"error ": "course doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    try:
        requester = Student.objects.get(user= user)
    except Student.DoesNotExist:
        try:
            requester  =Instructor.objects.get(user =  user)
            if course.instructor != requester:
                return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return getM3U8(courseId,lectureId)
        except Instructor.DoesNotExist:
            return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
    #check if student is enrollend in course
    if not requester.registeredCourses.filter(id=course.id).exists():
        return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    return getM3U8(courseId,lectureId)


def getM3U8(courseId,lectureId):
    segmentName = 'output.m3u8'
    try:
        lecture = Lecture.objects.get(id = lectureId)
    except:
        return Response({'error':"lecture doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    
    hls_dir = os.path.join(settings.MEDIA_ROOT, 'LectureVideos', f'{lecture.title}_{lectureId}')
    hls_file_path = os.path.join(hls_dir, segmentName)


    if os.path.exists(hls_file_path):
        with open(hls_file_path, 'rb') as hls_file:
            data = hls_file.read()
            print(data)
            content_type = 'audio/mpegurl'
            st = status.HTTP_200_OK 
            response = HttpResponse(data, content_type=content_type, status=st)
            return response
    return Response({'message':hls_file_path},status=status.HTTP_404_NOT_FOUND)



# maybe this does not need authorization because we only allow access to the playlist on authorization 
# maybe we can add salt or hash while we create hls playlist to make the segment names more secure and trustworthy 
# removed auth on both sides will have to depend on auth from the client 
# create a function in the client side and a view here to check if the user has access 
# not the best approach but better than no auth 
# found a work around add auth here also
# This view is working perfectly while checking on every request whether the user is authorized or not now
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def playLecture(request,courseId,lectureId, segmentName ):
    user = request.user
    print(user)
    try:
        lecture = Lecture.objects.get(id = lectureId)
    except:
        return Response({'error':"lecture doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    hls_dir = os.path.join(settings.MEDIA_ROOT, 'LectureVideos', f'{lecture.title}_{lectureId}')
    hls_file_path = os.path.join(hls_dir, segmentName)
    # print(request.headers)
    user = request.user
    try:
        course = Course.objects.get(id= courseId)
    except Course.DoesNotExist:
        return Response({"error ": "course doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    try:
        requester = Student.objects.get(user= user)
    except Student.DoesNotExist:
        try:
            requester  =Instructor.objects.get(user =  user)
            if course.instructor != requester:
                return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return getM3U8(courseId,lectureId)
        except Instructor.DoesNotExist:
            return Response({"error" :"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
    #check if student is enrollend in course
    if not requester.registeredCourses.filter(id=course.id).exists():
        return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
    if os.path.exists(hls_file_path):
        with open(hls_file_path, 'rb') as hls_file:
            data = hls_file.read()
            content_type = 'audio/mpegurl' if segmentName == 'output.m3u8' else 'application/octet-stream'
            st = status.HTTP_200_OK if segmentName == 'output.m3u8' else status.HTTP_206_PARTIAL_CONTENT
            response = HttpResponse(data, content_type=content_type, status=st)
            return response
    return Response({'message':hls_file_path},status=status.HTTP_404_NOT_FOUND)