from django.shortcuts import render, redirect
from billapp.forms import NewBill, UserForm, UserProfileInfoForm
from billapp.models import bill
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from .filters import UserFilter
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMessage, send_mail

from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
import django
from django.conf import settings
from django.core.mail import send_mail
import datetime


# Create your views here.

def index(request):
	return render(request, 'billapp/index.html', )


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				messages.add_message(request, messages.INFO, "Account Inactive. Contact WSDC.")

		else:
			print("Someone tried to login and failed!")
			print("Username: {} and password: {}".format(username, password))
			messages.add_message(request, messages.INFO, "Incorrect username or password")

	return render(request, 'billapp/login.html', {})


def check_bill_status(request):
	serial_no = request.GET.get('serial_no', None)
	context = {}

	if serial_no is None or serial_no == "":
		messages.add_message(request, messages.ERROR, "Enter a valid Reference ID")
	else:
		bill_ob = bill.objects.filter(bill_no=serial_no)
		if not bill_ob.exists():
			messages.add_message(request, messages.ERROR, "No bill with that Reference ID found.")
		else:
			context['bill'] = bill_ob.first()

	return render(request, 'billapp/login.html', context)


def register(request):
	registered = False

	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileInfoForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'profile_pic' in request.FILES:
				profile.profile_pic = request.FILES['profile_pic']

			profile.save()

			registered = True

		else:
			print(user_form.errors, profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()

	return render(request, 'billapp/registeration.html',
	              {'user_form': user_form,
	               'profile_form': profile_form,
	               'registered': registered})


@login_required
def status_list(request):
	date = request.GET.get("date", None)
	bill_no = request.GET.get("bill_no", None)
	bill_list = bill.objects.order_by('-date_on_doc')

	if bill_no is not None:
		bill_list = bill_list.filter(bill_no=int(bill_no))
	else:
		if date is not None:
			bill_list = bill_list.filter(date_on_doc=date)
		else:
			bill_list = bill_list.filter(date_on_doc=timezone.now().date())

	date_dic = {'bill_records': bill_list, 'today_fmt': timezone.now().date().strftime("%Y-%m-%d"), 'today_str': timezone.now().date(), 'bill_no': bill_no}
	return render(request, 'billapp/status.html', context=date_dic)


@login_required
def newbill(request):
	form = NewBill()

	if request.method == "POST":
		form = NewBill(request.POST)

		if form.is_valid():
			send_to = request.POST.get('email')
			form.save(commit=True)
			instance = form.instance
			print("Form validated. Sending mails.")
			send_mails(request, instance, True)
			return redirect('/')

		else:
			print('ERROR')

	return render(request, 'billapp/form.html', {'form': form})


def send_mails(request, instance, is_new_bill):
	send_to = instance.email
	beneficiary_email = request.POST.get('beneficiary_email')
	amt = str(instance.bill_amount)
	dmn = settings.DOMAIN_NAME
	ref = str(instance.bill_no)

	if is_new_bill:
		body = 'Your bill amounting to INR' + amt + ' has been received at Accounts Section, NIT Warangal. Visit ' + dmn + '/public' + ' and use the bill reference ID give below to check bill status.'
		body += '<br/><br/> Bill Reference ID: <b>' + ref + '</b>'
		body += '<br><br>Accounts Section<br>NIT Warangal<br>Telangana - 506004'
	else:
		body = 'Status of your bill at Accounts Section, NIT Warangal has been updated. Visit ' + dmn + '/public' + ' and use the bill reference ID give below to check the same.'
		body += '<br/><br/> Bill Reference ID: <b>' + ref + '</b>'
		body += '<br><br>Accounts Section<br>NIT Warangal<br>Telangana - 506004'

	# email = EmailMessage('Update from Accounts, NIT Warangal', body, to=[send_to, beneficiary_email])
	# email.send()

	send_mail(
		'Update from Accounts Section, NIT Warangal',
		'',
		'wsdcbills@gmail.com',
		[send_to, beneficiary_email],
		fail_silently=False,
		html_message=body
	)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')


@login_required
def update(request):
	id = request.POST['serial_no']
	instance = bill.objects.get(serial_no=id)
	form = NewBill(request.POST or None, instance=instance)
	status_changed = False
	if form.is_valid():
		if bill.objects.get(serial_no=id).status != form.cleaned_data['status']:
			status_changed = True
		form.save()
		if status_changed:
			print("Sending mails")
			instance = bill.objects.get(serial_no=id)
			send_mails(request, instance, False)
	else:
		messages.add_message(request, messages.ERROR, str(form.errors))
	return redirect('/')
