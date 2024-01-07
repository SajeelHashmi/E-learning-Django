from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from Student.models import Student
from Instructor.models import Instructor
from Notifications.models import Notification
from IlmGhar.emailAlerts import signUpMsg
# token.get_or_create(user = user) checks wether a token exists against a certain user and then deletes that token 


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        phoneNum = request.data.get('phoneNum')
        name = request.data.get('name')

        try:
            existing_user = User.objects.get(email=email)
            return Response({"error":"Email already in use"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass
        if email and username and password and password2 and phoneNum and name:
            if password == password2:
                user_data = {
                        'username': username,  
                        'password': password,  
                        'email': email,  
                        }
                user = User.objects.create_user(**user_data)
                Student.objects.create(user = user,phoneNumber=phoneNum,name = name)
                token, created = Token.objects.get_or_create(user=user)
                signUpMsg(email=email,name=name)
                return Response({
                    'token': token.key,
                    'userName': name,
                    'notificationCount':0
                    })
            else:
                return Response({"error":"passwords donot match"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"incomplete information"}, status=status.HTTP_400_BAD_REQUEST)
       
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        try:
            student = Student.objects.get(user = user)
            notificationCount = Notification.objects.filter(user = user,read = False).count()
            print("notificationCount",notificationCount)
            if created:
                token.delete()
                token ,created = Token.objects.get_or_create(user = user)
            return Response({
                'token': token.key,
                "INS":False,
                'userName':student.name,
                'notificationCount':notificationCount

                },)            
        except:
            try:
                instructor = Instructor.objects.get(user = user)
                notificationCount = Notification.objects.filter(user = user,read = False).count()
                print(notificationCount)
                if created:
                    token.delete()
                    token ,created = Token.objects.get_or_create(user = user)
                return Response({
                    'token': token.key,
                    "INS":True,
                    'userName':instructor.name,
                    'notificationCount':notificationCount
                    },)   
                       
            except:
                token.delete()
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def logout(request):
    key = request.data.get("token")
    if key:
        try:
            token = Token.objects.get(key=key)
            token.delete()
            return Response({"success": "Logged out successfully"})

        except Token.DoesNotExist:
            return Response({"error": "Token not found"})
    return Response({"error": "Token not provided"})