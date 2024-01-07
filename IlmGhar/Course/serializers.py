from rest_framework import serializers
from .models import Course,Tag,Language,Subject,Lecture,Assignment
from Student.models import Submissions
import base64
from Instructor.instructorSerializer import instructorSerializer



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name',)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name',)

class SerializerCourseCard(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    coverPicBlob = serializers.SerializerMethodField()
    instructorName = serializers.SerializerMethodField()
    language = LanguageSerializer(many=False, read_only=True)
    subject = SubjectSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id','description','title','coverPicBlob','tags',"language",'subject','instructorName']
    def get_coverPicBlob(self, obj):
        if obj.coverPic:
            with open(obj.coverPic.path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return f'data:image/jpeg;base64,{encoded_image}'
        return None
    def get_instructorName(self,obj):
        if obj.instructor:
            return obj.instructor.name
        

class CourseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    coverPicBlob = serializers.SerializerMethodField()
    instructor = instructorSerializer(read_only = True)
    class Meta:
        model = Course
        fields = ['id','description','title','coverPicBlob','tags','subject','language','instructor']
    def get_coverPicBlob(self, obj):
        if obj.coverPic:
            with open(obj.coverPic.path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return f'data:image/jpeg;base64,{encoded_image}'
        return None


class SubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissions
        fields = ['checked','remarks','marksObt']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields =['title','marks','id']



class LectureSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(many = False,read_only = True)
    class Meta:
        model = Lecture
        fields  = ['id','number','title','description','assignment']

class RegisterCourseSerializer(serializers.ModelSerializer):
    coverPicBlob = serializers.SerializerMethodField()
    lectures =  serializers.SerializerMethodField()
    language = LanguageSerializer(many=False, read_only=True)
    subject = SubjectSerializer(many=False, read_only=True)
    instructor = instructorSerializer(read_only = True)
    class Meta:
        model = Course
        fields = ['id','description','title','coverPicBlob','tags',"language",'subject','instructor','lectures']
    def get_coverPicBlob(self, obj):
        if obj.coverPic:
            with open(obj.coverPic.path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return f'data:image/jpeg;base64,{encoded_image}'
        return None
    def get_lectures(self,obj):
        lectures = Lecture.objects.filter(course = obj)
        if not lectures:
            return None
        return LectureSerializer(lectures,many=True).data

