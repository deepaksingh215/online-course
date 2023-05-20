from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        
        # Check for existing users with the same email
        while CustomUser.objects.filter(email=email).exists():
            # Append a UUID to make the email unique
            email = f"{email}-{uuid.uuid4().hex[:6]}"
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15)

    objects = CustomUserManager()

class ContactUs(models.Model):
    email = models.EmailField()
    contact_no = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15)

    

class Course(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="files/thumbnail")
    date = models.DateTimeField(auto_now_add=True)
    length = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    description = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UserCourse(models.Model):
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.name
        # return f'{self.user.username} - {self.course.name}'


class Video(models.Model):
    title = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video_file = models.FileField(upload_to='videos/')
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Payment(models.Model):
    order_id = models.CharField(max_length = 50 , null = False)
    payment_id = models.CharField(max_length = 50)
    user_course = models.ForeignKey(UserCourse , null = True , blank = True ,  on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser ,  on_delete=models.CASCADE)
    course = models.ForeignKey(Course , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

   