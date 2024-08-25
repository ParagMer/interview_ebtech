from django.contrib import admin
from django.urls import path, include
from etech_app.views import users_login, dashboard, product_api
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', users_login, name='login'),
    path('index/', dashboard, name='index'),
    path('api/', include('etech_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])