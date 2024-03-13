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
from django.urls import path, include, re_path
from django.conf import settings, urls
from django.conf.urls.static import static
from django.contrib.auth import logout, views 
from .views import index, Error404, Error505, Error403
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('deuda', include('apps.deuda.urls')),
    path('legajo/', include('apps.legajo.urls')),
    path('lote/', include('apps.lote.urls')),
    path('movimiento/', include('apps.movimiento.urls')),
    path('prioridad/', include('apps.prioridad.urls')),
    path('rec_lote/', include('apps.rec_lote.urls')),
    path('rec_prioridad/', include('apps.rec_prioridad.urls')),
    path('reclamo/', include('apps.reclamo.urls')),
    path('std_mov/', include('apps.std_mov.urls')),
    path('tipo_reclamo/', include('apps.tipo_reclamo.urls')),
    path('estado/', include('apps.estado.urls')),
    path('control_std/', include('apps.control_std.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('informes/', include('apps.informes.urls')),
    path('', index, name='index'),
    path("accounts/", include("django.contrib.auth.urls"),name='login'),
    path('accounts/logout/', logout,name='logout'),
    path('accounts/password_change/', views.PasswordChangeView.as_view() ,name='cambiar_pass'),
    path('config/password-change/done/',views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('administrador/', include('apps.administrador.urls')),
    path('rol/', include('apps.rol.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urls.handler404 = Error404.as_view()
urls.handler500 = Error505.as_error_view()
#urls.handler403 = Error403.as_view()



