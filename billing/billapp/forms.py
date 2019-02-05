from django import forms
from billapp.models import bill,UserProfileInfo
from django.contrib.auth.models import User
from django.utils import timezone


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

    current_date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now(), disabled=True)
    date_on_doc = forms.DateField(widget=forms.SelectDateWidget(years=range(2017, timezone.now().year + 1)))

# class MyForm(forms.ModelForm):
#     class Meta:
#         model = MyModel
