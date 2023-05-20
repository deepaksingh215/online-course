from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, CourseSerializer,ContactUsSerializer,UserCourseSerializer, CoursePageSerializer, VideoSerializer, PaymentSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from .models import Course, ContactUs, Course, Video, UserCourse,Payment
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import requests
from time import time
from django.views.decorators.csrf import csrf_exempt
from NewAssignment.settings import *

import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None) 
    

class HomePageAPIView(APIView):
    def get(self, request, format=None):
        courses = Course.objects.filter(active=True)
        contact = ContactUs.objects.all()
        course_serializer = CourseSerializer(courses, many=True)
        contact_serializer = ContactUsSerializer(contact, many=True)
        
        
        response_data = {
            'courses': course_serializer.data ,
            'contacts': contact_serializer.data
        }

        return Response(response_data)


class MyCoursesListAPIView(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 

    def get(self, request, format=None):
        user_courses = UserCourse.objects.filter(user=request.user)
        serializer = UserCourseSerializer(user_courses, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def coursePageAPI(request, slug):
    course = Course.objects.get(slug=slug)
    # Other logic for retrieving videos, serial number, etc.

    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")

    try:
            video = videos.get(serial_number=serial_number)
    except Video.DoesNotExist:
        video = None

    if video and not video.is_preview:
        if not request.user.is_authenticated:
            return redirect("login")
        
        user = request.user
        try:    
            user_course = UserCourse.objects.get(user=user, course=course)
        except UserCourse.DoesNotExist:
            return redirect("buy-now", slug=course.slug)
    
    course_data = {
            'course': CourseSerializer(course).data,
            'video': VideoSerializer(video).data if video else None,
            'videos': VideoSerializer(videos, many=True).data,
        }
    
    return Response(course_data)




class BuyNowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        course = Course.objects.get(slug=slug)
        user = request.user
        action = request.GET.get('action')
        order = None
        payment = None
        error = None

        try:
            user_course = UserCourse.objects.get(user=user, course=course)
            error = "You are Already Enrolled in this Course"
        except UserCourse.DoesNotExist:
            pass

        amount = None
        if error is None:
            amount = int((course.price - (course.price * course.discount * 0.01)) * 100)

        if amount == 0:
            user_course = UserCourse(user=user, course=course)
            user_course.save()
            return redirect('my-courses')

        if action == 'create_payment':
            currency = "INR"
            notes = {
                "email" : user.email, 
                "name" : f'{user.first_name} {user.last_name}'
            }
            reciept = f"course-{int(time())}"
            
            order = client.order.create(
                {'receipt' :reciept , 
                'notes' : notes , 
                'amount' : amount ,
                'currency' : currency
                }
            )

            payment = Payment()
            payment.user = user
            payment.course = course
            payment.order_id = order.get('id')
            payment.save()

        context = {
            "course": CourseSerializer(course).data,
            "order": order,
            "payment": payment,
            "user": user,
            "error": error
        }
        return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def verifyPaymentAPI(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id  = razorpay_payment_id
            payment.status =  True
            
            userCourse = UserCourse(user = payment.user , course = payment.course)
            userCourse.save()

            print("UserCourse" ,  userCourse.id)

            payment.user_course = userCourse
            payment.save()

            return Response({'message': 'Payment verified successfully'})

        except:
            return Response({'message': 'Invalid Payment Details'})
