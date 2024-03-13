"""
URL configuration for inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings, urls
from django.conf.urls.static import static
from django.contrib.auth import logout, views 
from .views import index, Error404, Error505


urlpatterns = [
    path('admin/', admin.site.urls),
    path('clase/', include('apps.clase.urls')),
    path('marca/', include('apps.marca.urls')),
    path('modelo/', include('apps.modelo.urls')),
    path('tipo/', include('apps.tipo.urls')),
    path('oficina/', include('apps.oficina.urls')),
    path('bien/', include('apps.bien.urls')),
    path('estado/', include('apps.estado.urls')),
    path('operador/', include('apps.operador.urls')),
    path('imagenes/', include('apps.imgbien.urls')),
    path('datas/', include('apps.movdata.urls')),
    path('', index, name='index'),
    path("accounts/", include("django.contrib.auth.urls"),name='login'),
    path('accounts/logout/', logout,name='logout'),
    path('accounts/password_change/', views.PasswordChangeView.as_view() ,name='cambiar_pass'),
    path('config/password-change/done/',views.PasswordChangeDoneView.as_view(), name='password_change_done')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urls.handler404 = Error404.as_view()
urls.handler500 = Error505.as_error_view()



