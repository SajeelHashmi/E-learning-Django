from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from Student.models import Student





#returns all the courses after applying filters
@api_view(['GET', 'POST'])
def courses(request):
    pass