from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('events.urls')),
    path('members/',include('django.contrib.auth.urls')),
    path('members/',include('members.urls')),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# configure admin title
admin.site.site_header="MyClub Adminstration"
admin.site.site_title="Browser title"
admin.site.index_title="Welcome to the admin area!"