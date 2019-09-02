from django.contrib import admin
from django.urls import path, include
# Uploaded Media Files
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('all_safe_xxx_safe_all/', admin.site.urls),
	path('invoice/', include('invoice.urls', namespace='invoice')),
	path('dashboard/', include('service.urls', namespace='service')),
	path('', include('user.urls', namespace='user')),

]


# Media files URL 
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)