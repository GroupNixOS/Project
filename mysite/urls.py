#mysite/mysite/

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    path('portal/', include('portal.urls')),
]
