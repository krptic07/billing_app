from django.conf.urls import url
from billapp import views

# app_name = 'billapp'


urlpatterns=[
    url(r'^$',views.status_list,name='status_list'),
    url(r'^newbill/',views.newbill,name='newbill'),
    url(r'^update ',views.update,name='update'),
    url(r'^register/',views.register,name='register'),
    url(r'^checkStatus/', views.check_bill_status, name='check_status'),

    url(r'public/',views.user_login,name='user_login'),
]
