from django.contrib import admin
from django.urls import path  , include
from django.conf.urls.static import static
from . import settings
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('store.urls'))
    #path('', lambda request: HttpResponse('the cow jumped over the moon')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
