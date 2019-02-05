from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username


class bill(models.Model):
    STATUS_CHOICES = [('pro','Processed'),
    ('unp','Under Process'),
    ('def','Deficiency in docs'),
    ('rec','Received In Accounts')]

    serial_no = models.AutoField(primary_key=True)
    current_date = models.DateField(("Date"), default=datetime.date.today)
    department_name = models.CharField(max_length=264)
    beneficiary_name = models.CharField(max_length=264)
    beneficiary_email = models.EmailField()
    bill_no = models.CharField(unique=True, max_length=100)
    date_on_doc = models.DateField()
    bill_amount = models.IntegerField(default=10)
    head_code = models.CharField(max_length=264)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    email= models.EmailField()
    mobile = models.IntegerField(default=10)
    remarks = models.TextField(null=True)

    def __str__(self):
        return str(self.bill_no)
