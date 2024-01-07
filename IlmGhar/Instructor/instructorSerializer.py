from rest_framework import serializers
from .models import Instructor
import base64

class instructorSerializer(serializers.ModelSerializer):
    pfpBlob = serializers.SerializerMethodField()
    class Meta:
        model = Instructor
        fields = ['name','bio','pfpBlob']
    def get_pfpBlob(self,obj):
        if obj.profilePic:
            with open(obj.profilePic.path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return f'data:image/jpeg;base64,{encoded_image}'
        return None
    
