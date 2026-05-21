from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bugs import views as bug_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bug_views.home, name='home'),
   # path('home/', bug_views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('bugs/', include('bugs.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)