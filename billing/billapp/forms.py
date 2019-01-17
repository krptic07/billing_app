from django import forms
from billapp.models import bill,UserProfileInfo
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)


class NewBill(forms.ModelForm):
    class Meta:
        model = bill
        fields = '__all__'

# class MyForm(forms.ModelForm):
#     class Meta:
#         model = MyModel
