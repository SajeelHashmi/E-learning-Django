from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Course ,Tag,Language,Subject
from .serializers import CourseSerializer, SerializerCourseCard,LanguageSerializer,SubjectSerializer,TagSerializer
from rest_framework.exceptions import AuthenticationFailed
from Student.models import Student 




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getRegistered(request,id:int):
    try:
        course = Course.objects.get(id = id)
    except:
        return Response({"error":"Course does not exist"},status=status.HTTP_404_NOT_FOUND)
    user = request.user
    serializer = CourseSerializer(course,many=False)
    try:
        student  = Student.objects.get(user = user)
    except Student.DoesNotExist:    
        return Response(serializer.data,status=status.HTTP_200_OK)
    if course in student.registeredCourses.all():
       return Response({"registered":True},status=status.HTTP_200_OK)
    return Response(serializer.data,status=status.HTTP_200_OK)
    

@api_view(['GET'])
def getCourse(request,id:int):
    try:
        course  = Course.objects.get(id= id)
    except:
        return Response({"error":"Course does not exist"},status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course,many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)
    

@api_view(['GET'])
def getLanguages(request):
    language = Language.objects.all()
    serializer = LanguageSerializer(language,many= True)
    return Response(serializer.data)
    
@api_view(['GET'])
def getSubjects(request):
    subject = Subject.objects.all()
    serializer = SubjectSerializer(subject,many= True)
    return Response(serializer.data)


@api_view(['GET'])
def getTags(request):
    tag = Tag.objects.all()
    serializer = TagSerializer(tag,many= True)
    return Response(serializer.data)


@api_view(['GET'])
def allCourses(request):
    page = request.GET.get('page')
   
        
    if page:
        if page.isnumeric():
            page  = int(page)
        else:
            page = 0
    else:
        page = 0
    print(page)
    # extract this functionality to seprate views for now it is working
    items_per_page = 30
    query = request.GET.get('q')
    id = request.GET.get("id")
    if id:
        try:
            course = Course.objects.get(id = id)
            print(course)
            serialized = CourseSerializer(course, many= False)
            return Response(serialized.data)
        except Course.DoesNotExist:
            return Response({"error":"course not found"},status=status.HTTP_404_NOT_FOUND)
    
    courses = Course.objects.all()
   
    if query:
        courses = courses.filter(title__icontains=query)

    start = (page - 1) * items_per_page if page and page > 0 else 0
    end = start + items_per_page
    courses = courses[start:end]
    serializer = SerializerCourseCard(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getFirstThreeByLanguage(request,language):
    lang = Language.objects.get(name = language)
    courses = Course.objects.filter(language = lang)[:3]
    serializer = SerializerCourseCard(courses, many=True)
    return Response(serializer.data)


