from rest_framework import serializers
from .models import Instructor
from Course.models import Course,Lecture,Assignment
from Student.models import Student,Submissions
from Student.serializers import studentSerializer
from .instructorSerializer import instructorSerializer
from Course.serializers import LanguageSerializer,LectureSerializer,SubjectSerializer,SubmissionsSerializer
import base64

    
#requirements for this id cover pic list of students lectures for each lecture assignments  
#and for each assignment a submission object containing student id and there submission if it exists#
class YourCourseSerializer(serializers.ModelSerializer):
    coverPicBlob = serializers.SerializerMethodField()
    language = LanguageSerializer(many=False, read_only=True)
    lectures = serializers.SerializerMethodField()
    subject = SubjectSerializer(many=False, read_only=True)
    instructor = instructorSerializer(read_only = True)
    class Meta:
        model = Course
        fields = ['id','description','title','coverPicBlob','tags',"language",'lectures','subject','instructor']
    def get_coverPicBlob(self, obj):
        if obj.coverPic:
            with open(obj.coverPic.path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return f'data:image/jpeg;base64,{encoded_image}'
        return None
  
  
    def get_lectures(self,obj):
        students = Student.objects.filter(registeredCourses=obj)
        if not students:
            return None
        lectures = Lecture.objects.filter(course = obj)
        if not lectures:
            return None
        lectures =  LectureSerializer(lectures,many=True).data
        for lecture in lectures:
            studentsArr = []
            for student  in  students:
                studentObj = {}
                studentData = studentSerializer(student,many=False).data
                assignmentid =   lecture['assignment']['id']
                print("assignmentid",assignmentid)
                assignment = Assignment.objects.get(id = assignmentid)
                try:
                    submission = Submissions.objects.get(assignment = assignment,student = student)
                    submissionData = SubmissionsSerializer(submission,many = False).data
                except Submissions.DoesNotExist:
                    submissionData = False
                studentObj['student'] = studentData
                studentObj['submission'] = submissionData
                print(studentObj['submission'])
                studentsArr.append(studentObj)
            print(studentsArr)

            lecture['assignment']['students'] = studentsArr
            print(lecture)
        return lectures


            




"""
course info
    lectures
        assignments
            students submissions
"""