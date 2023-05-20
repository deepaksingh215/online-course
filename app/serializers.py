from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id','username', 'first_name', 'last_name', 'email' ,
            'contact_no', 'whatsapp'
        )

class RegisterSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(write_only=True)
    confirm_email = serializers.EmailField(write_only=True)
    contact_no = serializers.CharField()
    whatsapp = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email',  'confirm_email', 'password','confirm_password', 
            'contact_no', 'whatsapp'
        )
        

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if attrs['email'] != attrs['confirm_email']:
            raise serializers.ValidationError("Emails do not match.")
        return attrs

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        confirm_email = validated_data.pop('confirm_email')

        if confirm_password is None or confirm_email is None:
            raise serializers.ValidationError("Confirmation data is missing.")
    
        if validated_data['password'] != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
    
        if validated_data['email'] != confirm_email:
            raise serializers.ValidationError("Emails do not match.")
        
        user = CustomUser.objects.create_user(**validated_data)
        return user




class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = '__all__'

class CoursePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
    
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'



class CourseSerializer(ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'slug', 'description', 'price', 'discount', 'active', 'thumbnail', 'date', 'length', 'videos']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
