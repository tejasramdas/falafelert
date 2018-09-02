from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'qwerty123^$', hello.views.run_search, name='run_search'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^deleteall', hello.views.dell, name='dell'),
    path('admin/', admin.site.urls),

]
