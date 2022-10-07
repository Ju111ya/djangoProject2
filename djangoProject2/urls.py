from idlelib.multicall import r

from django.conf.urls.i18n import i18n_patterns
from django.template.defaulttags import url
from siteAlb import *
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from siteAlb import views

urlpatterns = [
    path('back/', views.stop_sim, name='back'),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('wrkng_sim', views.sim_running, name='working_sim'),
    path('siteAlb/', include('siteAlb.urls')),
    path('', views.home_view, name='home'),
)

