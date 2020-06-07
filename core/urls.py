from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^register/$',views.signup_view,name='register'),
    url(r'^login/$',views.signin_view,name='login'),
    url(r'^logout/$',views.signout_view,name='logout'),
    url(r'^contact/$',views.contact_view,name='team'),
    url(r'^admin-home/$',views.add_home_view,name='admin_home'),
    url(r'^admin-home/(?P<pk>\d+)$',views.receipt_view,name='recepit_view'),

]

