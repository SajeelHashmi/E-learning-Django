from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post
from Student.serializers import studentSerializer
from Student.models import Student
from Instructor.models import Instructor


#check if user is a student if yes just use the student Serializer other wise create a simple serializer for instructor 
# also maybe sent the fact that if it is an instructor post or not so it can be highlighted 
class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    repliesNum = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('content', 'id','user','repliesNum')

    def get_user(self,obj):
        try:
            user = Student.objects.get(user = obj.user)
        except Student.DoesNotExist:
            try:
                user = Instructor.objects.get(user = obj.user)
            except:
                return None
        return user.name

    def get_repliesNum(self,obj):
        return Post.objects.filter(parent = obj).count()

